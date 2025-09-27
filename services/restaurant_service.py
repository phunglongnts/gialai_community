from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
import models
import schemas
import logging

logger = logging.getLogger(__name__)


class RestaurantService:
    def __init__(self):
        pass

    def create_restaurant(self, db: Session, restaurant: schemas.RestaurantCreate) -> models.Restaurant:
        """Tạo nhà hàng mới"""
        try:
            db_restaurant = models.Restaurant(
                name=restaurant.name,
                description=restaurant.description,
                category=restaurant.category,
                address=restaurant.address,
                phone=restaurant.phone,
                email=restaurant.email,
                website=restaurant.website,
                latitude=restaurant.latitude,
                longitude=restaurant.longitude,
                business_hours=restaurant.business_hours or {},
                price_range=restaurant.price_range,
                average_price=restaurant.average_price,
                features=restaurant.features or [],
                cuisine_types=restaurant.cuisine_types or [],
                owner_id=restaurant.owner_id
            )

            db.add(db_restaurant)
            db.commit()
            db.refresh(db_restaurant)
            return db_restaurant

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating restaurant: {str(e)}")
            raise e

    def get_restaurant(self, db: Session, restaurant_id: int) -> Optional[models.Restaurant]:
        """Lấy thông tin nhà hàng theo ID"""
        return db.query(models.Restaurant).filter(
            models.Restaurant.id == restaurant_id,
            models.Restaurant.is_active == True
        ).first()

    def get_restaurants(self, db: Session, skip: int = 0, limit: int = 10,
                        category: Optional[str] = None) -> List[models.Restaurant]:
        """Lấy danh sách nhà hàng"""
        query = db.query(models.Restaurant).filter(models.Restaurant.is_active == True)

        if category:
            query = query.filter(models.Restaurant.category == category)

        return query.offset(skip).limit(limit).all()

    def search_restaurants(self, db: Session, filters: schemas.RestaurantSearchFilters,
                           skip: int = 0, limit: int = 10) -> List[models.Restaurant]:
        """Tìm kiếm nhà hàng với bộ lọc"""
        query = db.query(models.Restaurant).filter(models.Restaurant.is_active == True)

        # Filter by category
        if filters.category:
            query = query.filter(models.Restaurant.category == filters.category)

        # Filter by price range
        if filters.price_range:
            query = query.filter(models.Restaurant.price_range == filters.price_range)

        # Filter by minimum rating
        if filters.min_rating:
            query = query.filter(models.Restaurant.average_rating >= filters.min_rating)

        # Filter by features
        if filters.features:
            for feature in filters.features:
                query = query.filter(models.Restaurant.features.contains([feature]))

        # Filter by cuisine types
        if filters.cuisine_types:
            cuisine_conditions = []
            for cuisine in filters.cuisine_types:
                cuisine_conditions.append(models.Restaurant.cuisine_types.contains([cuisine]))
            query = query.filter(or_(*cuisine_conditions))

        # Distance filtering (if coordinates provided)
        if (filters.user_lat and filters.user_lng and
                filters.max_distance and filters.max_distance > 0):
            # Simple distance calculation using Haversine formula
            # In production, consider using PostGIS for better performance
            query = query.filter(
                and_(
                    models.Restaurant.latitude.isnot(None),
                    models.Restaurant.longitude.isnot(None)
                )
            )

        return query.offset(skip).limit(limit).all()

    def update_restaurant(self, db: Session, restaurant_id: int,
                          restaurant_update: schemas.RestaurantUpdate) -> Optional[models.Restaurant]:
        """Cập nhật thông tin nhà hàng"""
        try:
            db_restaurant = self.get_restaurant(db, restaurant_id)
            if not db_restaurant:
                return None

            update_data = restaurant_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_restaurant, field, value)

            db.commit()
            db.refresh(db_restaurant)
            return db_restaurant

        except Exception as e:
            db.rollback()
            logger.error(f"Error updating restaurant {restaurant_id}: {str(e)}")
            raise e

    def delete_restaurant(self, db: Session, restaurant_id: int) -> bool:
        """Xóa nhà hàng (soft delete)"""
        try:
            db_restaurant = self.get_restaurant(db, restaurant_id)
            if not db_restaurant:
                return False

            db_restaurant.is_active = False
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting restaurant {restaurant_id}: {str(e)}")
            return False

    def create_review(self, db: Session, review: schemas.ReviewCreate) -> models.Review:
        """Tạo đánh giá mới"""
        try:
            # Kiểm tra nhà hàng tồn tại
            restaurant = self.get_restaurant(db, review.restaurant_id)
            if not restaurant:
                raise ValueError("Nhà hàng không tồn tại")

            # Tạo review
            db_review = models.Review(
                restaurant_id=review.restaurant_id,
                user_id=review.user_id,
                rating=review.rating,
                title=review.title,
                content=review.content,
                food_rating=review.food_rating,
                service_rating=review.service_rating,
                ambiance_rating=review.ambiance_rating,
                value_rating=review.value_rating,
                visit_date=review.visit_date,
                visit_type=review.visit_type,
                party_size=review.party_size,
                is_anonymous=review.is_anonymous
            )

            db.add(db_review)
            db.commit()

            # Cập nhật rating trung bình của nhà hàng
            self.update_restaurant_rating(db, review.restaurant_id)

            db.refresh(db_review)
            return db_review

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating review: {str(e)}")
            raise e

    def update_restaurant_rating(self, db: Session, restaurant_id: int):
        """Cập nhật rating trung bình của nhà hàng"""
        try:
            # Tính toán rating mới
            rating_stats = db.query(
                func.avg(models.Review.rating).label('avg_rating'),
                func.count(models.Review.id).label('total_reviews')
            ).filter(models.Review.restaurant_id == restaurant_id).first()

            # Cập nhật nhà hàng
            db_restaurant = db.query(models.Restaurant).filter(
                models.Restaurant.id == restaurant_id
            ).first()

            if db_restaurant and rating_stats:
                db_restaurant.average_rating = round(rating_stats.avg_rating or 0.0, 1)
                db_restaurant.total_reviews = rating_stats.total_reviews or 0
                db.commit()

        except Exception as e:
            logger.error(f"Error updating restaurant rating {restaurant_id}: {str(e)}")

    def get_restaurant_reviews(self, db: Session, restaurant_id: int,
                               skip: int = 0, limit: int = 10) -> List[models.Review]:
        """Lấy danh sách đánh giá của nhà hàng"""
        return db.query(models.Review).filter(
            models.Review.restaurant_id == restaurant_id
        ).order_by(models.Review.created_at.desc()).offset(skip).limit(limit).all()

    def create_search_context(self, restaurants: List[models.Restaurant]) -> str:
        """Tạo context cho AI từ danh sách nhà hàng"""
        context_data = []

        for restaurant in restaurants:
            restaurant_info = {
                'id': restaurant.id,
                'name': restaurant.name,
                'category': restaurant.category,
                'description': restaurant.description or "Không có mô tả",
                'address': restaurant.address,
                'price_range': restaurant.price_range or "Chưa xác định",
                'average_rating': restaurant.average_rating,
                'total_reviews': restaurant.total_reviews,
                'features': restaurant.features or [],
                'cuisine_types': restaurant.cuisine_types or [],
                'phone': restaurant.phone,
                'average_price': restaurant.average_price
            }
            context_data.append(restaurant_info)

        # Format context cho AI
        context = "DANH SÁCH NHÀ HÀNG:\n\n"

        for i, restaurant in enumerate(context_data, 1):
            context += f"{i}. **{restaurant['name']}** (ID: {restaurant['id']})\n"
            context += f"   📍 Địa chỉ: {restaurant['address']}\n"
            context += f"   🍽️ Loại: {restaurant['category']}\n"
            context += f"   💰 Giá: {restaurant['price_range']}"

            if restaurant['average_price']:
                context += f" (~{restaurant['average_price']:,} VND/người)"
            context += "\n"

            context += f"   ⭐ Đánh giá: {restaurant['average_rating']}/5.0 ({restaurant['total_reviews']} reviews)\n"
            context += f"   📝 Mô tả: {restaurant['description']}\n"

            if restaurant['cuisine_types']:
                context += f"   🥘 Món ăn: {', '.join(restaurant['cuisine_types'])}\n"

            if restaurant['features']:
                context += f"   ✨ Tiện ích: {', '.join(restaurant['features'])}\n"

            if restaurant['phone']:
                context += f"   📞 SĐT: {restaurant['phone']}\n"

            context += "\n" + "─" * 50 + "\n\n"

        return context

    def get_restaurant_analytics(self, db: Session, restaurant_id: int) -> Dict[str, Any]:
        """Lấy thống kê của nhà hàng"""
        try:
            restaurant = self.get_restaurant(db, restaurant_id)
            if not restaurant:
                return {}

            # Thống kê đánh giá theo sao
            rating_distribution = db.query(
                models.Review.rating,
                func.count(models.Review.id).label('count')
            ).filter(
                models.Review.restaurant_id == restaurant_id
            ).group_by(models.Review.rating).all()

            rating_dist = {str(i): 0 for i in range(1, 6)}
            for rating, count in rating_distribution:
                rating_dist[str(rating)] = count

            # Đánh giá gần đây
            recent_reviews = self.get_restaurant_reviews(db, restaurant_id, 0, 5)

            # Từ khóa phổ biến (đơn giản)
            all_reviews = db.query(models.Review.content).filter(
                models.Review.restaurant_id == restaurant_id
            ).all()

            # Phân tích từ khóa đơn giản
            keywords = self.extract_keywords_from_reviews([r.content for r in all_reviews])

            return {
                'restaurant_id': restaurant_id,
                'total_reviews': restaurant.total_reviews,
                'average_rating': restaurant.average_rating,
                'rating_distribution': rating_dist,
                'recent_reviews': len(recent_reviews),
                'top_keywords': keywords[:10]
            }

        except Exception as e:
            logger.error(f"Error getting restaurant analytics {restaurant_id}: {str(e)}")
            return {}

    def extract_keywords_from_reviews(self, review_contents: List[str]) -> List[str]:
        """Trích xuất từ khóa từ các đánh giá (phương pháp đơn giản)"""
        try:
            # Từ khóa phổ biến trong đánh giá nhà hàng
            positive_keywords = [
                'ngon', 'tốt', 'tuyệt vời', 'hài lòng', 'thích', 'ưng ý',
                'chất lượng', 'tuyệt', 'xuất sắc', 'hoàn hảo', 'ổn'
            ]

            negative_keywords = [
                'dở', 'tệ', 'không ngon', 'thất vọng', 'kém', 'tồi',
                'chậm', 'lạnh', 'mặn', 'nhạt', 'cháy'
            ]

            food_keywords = [
                'phở', 'bún', 'cơm', 'bánh', 'canh', 'gỏi', 'nướng',
                'xào', 'luộc', 'chiên', 'soup', 'salad', 'pasta'
            ]

            service_keywords = [
                'phục vụ', 'nhân viên', 'thái độ', 'nhiệt tình', 'chu đáo',
                'nhanh', 'chậm', 'thân thiện', 'lịch sự'
            ]

            all_keywords = positive_keywords + negative_keywords + food_keywords + service_keywords

            # Đếm frequency
            keyword_count = {}
            for content in review_contents:
                if content:
                    content_lower = content.lower()
                    for keyword in all_keywords:
                        if keyword in content_lower:
                            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1

            # Sort by frequency
            sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
            return [keyword for keyword, count in sorted_keywords if count >= 2]

        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []

    def get_popular_restaurants(self, db: Session, limit: int = 10) -> List[models.Restaurant]:
        """Lấy danh sách nhà hàng phổ biến"""
        return db.query(models.Restaurant).filter(
            models.Restaurant.is_active == True
        ).order_by(
            models.Restaurant.average_rating.desc(),
            models.Restaurant.total_reviews.desc()
        ).limit(limit).all()

    def get_nearby_restaurants(self, db: Session, lat: float, lng: float,
                               radius_km: float = 5.0, limit: int = 10) -> List[models.Restaurant]:
        """Lấy nhà hàng gần đó (tính toán đơn giản)"""
        # Đây là tính toán đơn giản, trong production nên dùng PostGIS
        restaurants = db.query(models.Restaurant).filter(
            and_(
                models.Restaurant.is_active == True,
                models.Restaurant.latitude.isnot(None),
                models.Restaurant.longitude.isnot(None)
            )
        ).all()

        # Filter by distance (simple calculation)
        nearby = []
        for restaurant in restaurants:
            if restaurant.latitude and restaurant.longitude:
                distance = self.calculate_distance(
                    lat, lng, restaurant.latitude, restaurant.longitude
                )
                if distance <= radius_km:
                    nearby.append((restaurant, distance))

        # Sort by distance
        nearby.sort(key=lambda x: x[1])
        return [restaurant for restaurant, distance in nearby[:limit]]

    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Tính khoảng cách giữa 2 điểm (Haversine formula)"""
        import math

        # Convert to radians
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])

        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        # Earth radius in kilometers
        r = 6371
        return r * c