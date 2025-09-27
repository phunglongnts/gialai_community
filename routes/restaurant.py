from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from database import get_db
from models import Restaurant, User, RatingDetail, Review, RestaurantAnalytics
from schemas import (
    RestaurantCreateRequest, RestaurantResponse, RestaurantListResponse,
    AIEnhancementRequest, AIEnhancementResponse, DashboardOverview,
    AnalyticsData, APIResponse, PaginatedResponse, MenuItemCreate,
    MenuItemResponse, ImageUploadResponse, BulkImageUploadResponse
)
from services.ai_enhancement_service import RestaurantAIEnhancementService
from services.auth_service import get_current_user, require_role
from services.file_service import FileUploadService
from utils.pagination import paginate
from utils.location_utils import geocode_address, calculate_distance

router = APIRouter(prefix="/restaurants", tags=["Quản lý nhà hàng"])

# Initialize services
ai_service = RestaurantAIEnhancementService()
file_service = FileUploadService()


# ================================
# Restaurant Creation Endpoints
# ================================

@router.post("/check-ownership", response_model=APIResponse)
async def check_restaurant_ownership(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Kiểm tra người dùng đã có nhà hàng chưa"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        has_restaurant = restaurant is not None

        return APIResponse(
            success=True,
            message="Đã kiểm tra quyền sở hữu nhà hàng" if has_restaurant else "Chưa có nhà hàng",
            data={
                "has_restaurant": has_restaurant,
                "restaurant_id": restaurant.id if restaurant else None,
                "restaurant_name": restaurant.name if restaurant else None
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi kiểm tra quyền sở hữu: {str(e)}"
        )


@router.post("/ai-enhance", response_model=AIEnhancementResponse)
async def enhance_restaurant_with_ai(
        request: AIEnhancementRequest,
        current_user: User = Depends(require_role("restaurant_owner"))
):
    """AI cải thiện thông tin nhà hàng trước khi tạo"""
    try:
        enhancement_result = await ai_service.enhance_restaurant_info(
            request.restaurant_data
        )

        return enhancement_result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi AI enhancement: {str(e)}"
        )


@router.post("/create", response_model=RestaurantResponse)
async def create_restaurant(
        restaurant_data: RestaurantCreateRequest,
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Tạo nhà hàng mới với AI enhancement"""
    try:
        # Kiểm tra user đã có nhà hàng chưa
        existing_restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if existing_restaurant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn đã có nhà hàng rồi. Mỗi tài khoản chỉ tạo được một nhà hàng."
            )

        # Geocoding địa chỉ để lấy tọa độ
        coordinates = None
        if restaurant_data.longitude is None or restaurant_data.latitude is None:
            coordinates = await geocode_address(restaurant_data.address)

        # AI Enhancement nếu enabled
        ai_enhanced_description = None
        ai_menu_suggestions = None
        ai_seo_content = None

        if restaurant_data.enable_ai_enhancement:
            enhancement_result = await ai_service.enhance_restaurant_info(restaurant_data)
            ai_enhanced_description = enhancement_result.enhanced_description
            ai_menu_suggestions = enhancement_result.menu_suggestions
            ai_seo_content = enhancement_result.seo_content

        # Tạo restaurant record
        new_restaurant = Restaurant(
            owner_id=current_user.id,
            name=restaurant_data.name,
            description=restaurant_data.description,
            ai_enhanced_description=ai_enhanced_description,
            cuisine_type=restaurant_data.cuisine_type,
            address=restaurant_data.address,
            province=restaurant_data.province,
            district=restaurant_data.district,
            ward=restaurant_data.ward,
            longitude=coordinates["longitude"] if coordinates else restaurant_data.longitude,
            latitude=coordinates["latitude"] if coordinates else restaurant_data.latitude,
            logo_url=restaurant_data.logo_url,
            cover_image_url=restaurant_data.cover_image_url,
            gallery_images=restaurant_data.gallery_images or [],
            opening_hours=restaurant_data.opening_hours or {},
            price_range=restaurant_data.price_range,
            facilities=restaurant_data.facilities or [],
            ai_menu_suggestions=ai_menu_suggestions,
            ai_seo_content=ai_seo_content,
            is_ai_enhanced=restaurant_data.enable_ai_enhancement,
            status="active"
        )

        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)

        # Tạo RatingDetail record cho nhà hàng mới
        rating_detail = RatingDetail(
            restaurant_id=new_restaurant.id,
            food_rating=0,
            service_rating=0,
            atmosphere_rating=0,
            price_rating=0,
            cleanliness_rating=0,
            overall_rating=0,
            total_reviews=0,
            positive_reviews=0,
            negative_reviews=0,
            neutral_reviews=0
        )

        db.add(rating_detail)
        db.commit()

        # Tạo analytics record đầu tiên
        today_analytics = RestaurantAnalytics(
            restaurant_id=new_restaurant.id,
            date=datetime.now(),
            page_views=0,
            unique_visitors=0,
            search_impressions=0,
            click_through_rate=0,
            avg_time_on_page=0,
            bounce_rate=0,
            top_keywords={}
        )

        db.add(today_analytics)
        db.commit()

        # Load restaurant với relationships để return
        restaurant_with_relations = db.query(Restaurant).filter(
            Restaurant.id == new_restaurant.id
        ).first()

        return RestaurantResponse.from_orm(restaurant_with_relations)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo nhà hàng: {str(e)}"
        )


# ================================
# File Upload Endpoints
# ================================

@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_restaurant_image(
        file: UploadFile = File(..., description="File ảnh (JPG, PNG, WebP)"),
        image_type: str = Form(..., description="Loại ảnh: logo, cover, gallery"),
        current_user: User = Depends(require_role("restaurant_owner"))
):
    """Upload ảnh cho nhà hàng"""
    try:
        # Validate image type
        allowed_types = ["logo", "cover", "gallery"]
        if image_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Loại ảnh không hợp lệ. Chọn từ: {allowed_types}"
            )

        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File phải là hình ảnh (JPG, PNG, WebP)"
            )

        # Upload file
        upload_result = await file_service.upload_image(
            file,
            folder=f"restaurants/{image_type}",
            max_size_mb=5  # 5MB limit
        )

        return ImageUploadResponse(
            success=True,
            url=upload_result["url"],
            filename=upload_result["filename"],
            size=upload_result["size"],
            content_type=file.content_type
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi upload ảnh: {str(e)}"
        )


@router.post("/upload-gallery", response_model=BulkImageUploadResponse)
async def upload_restaurant_gallery(
        files: List[UploadFile] = File(..., description="Danh sách ảnh gallery"),
        current_user: User = Depends(require_role("restaurant_owner"))
):
    """Upload nhiều ảnh gallery cùng lúc"""
    try:
        if len(files) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chỉ được upload tối đa 10 ảnh cùng lúc"
            )

        uploaded_images = []
        failed_uploads = []

        for file in files:
            try:
                if not file.content_type.startswith("image/"):
                    failed_uploads.append({
                        "filename": file.filename,
                        "error": "File không phải là hình ảnh"
                    })
                    continue

                upload_result = await file_service.upload_image(
                    file,
                    folder="restaurants/gallery",
                    max_size_mb=5
                )

                uploaded_images.append(ImageUploadResponse(
                    success=True,
                    url=upload_result["url"],
                    filename=upload_result["filename"],
                    size=upload_result["size"],
                    content_type=file.content_type
                ))

            except Exception as e:
                failed_uploads.append({
                    "filename": file.filename,
                    "error": str(e)
                })

        return BulkImageUploadResponse(
            success=len(uploaded_images) > 0,
            uploaded_images=uploaded_images,
            failed_uploads=failed_uploads,
            total_uploaded=len(uploaded_images)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi upload gallery: {str(e)}"
        )


# ================================
# Restaurant Management Endpoints
# ================================

@router.get("/my-restaurant", response_model=RestaurantResponse)
async def get_my_restaurant(
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Lấy thông tin nhà hàng của tôi"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bạn chưa có nhà hàng nào"
            )

        return RestaurantResponse.from_orm(restaurant)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy thông tin nhà hàng: {str(e)}"
        )


@router.put("/my-restaurant", response_model=RestaurantResponse)
async def update_my_restaurant(
        restaurant_data: RestaurantCreateRequest,
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Cập nhật thông tin nhà hàng của tôi"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Update basic info
        restaurant.name = restaurant_data.name
        restaurant.description = restaurant_data.description
        restaurant.cuisine_type = restaurant_data.cuisine_type
        restaurant.address = restaurant_data.address
        restaurant.province = restaurant_data.province
        restaurant.district = restaurant_data.district
        restaurant.ward = restaurant_data.ward
        restaurant.price_range = restaurant_data.price_range
        restaurant.facilities = restaurant_data.facilities or []
        restaurant.opening_hours = restaurant_data.opening_hours or {}

        # Update coordinates if changed
        if restaurant_data.longitude and restaurant_data.latitude:
            restaurant.longitude = restaurant_data.longitude
            restaurant.latitude = restaurant_data.latitude
        elif restaurant.address != restaurant_data.address:
            # Geocode new address
            coordinates = await geocode_address(restaurant_data.address)
            if coordinates:
                restaurant.longitude = coordinates["longitude"]
                restaurant.latitude = coordinates["latitude"]

        # Update images if provided
        if restaurant_data.logo_url:
            restaurant.logo_url = restaurant_data.logo_url
        if restaurant_data.cover_image_url:
            restaurant.cover_image_url = restaurant_data.cover_image_url
        if restaurant_data.gallery_images:
            restaurant.gallery_images = restaurant_data.gallery_images

        # AI Enhancement if enabled
        if restaurant_data.enable_ai_enhancement:
            enhancement_result = await ai_service.enhance_restaurant_info(restaurant_data)
            restaurant.ai_enhanced_description = enhancement_result.enhanced_description
            restaurant.ai_menu_suggestions = enhancement_result.menu_suggestions
            restaurant.ai_seo_content = enhancement_result.seo_content
            restaurant.is_ai_enhanced = True

        restaurant.updated_at = datetime.now()

        db.commit()
        db.refresh(restaurant)

        return RestaurantResponse.from_orm(restaurant)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi cập nhật nhà hàng: {str(e)}"
        )


@router.delete("/my-restaurant", response_model=APIResponse)
async def delete_my_restaurant(
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Xóa nhà hàng của tôi"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Soft delete - chỉ đổi status thay vì xóa hẳn
        restaurant.status = "deleted"
        restaurant.updated_at = datetime.now()

        db.commit()

        return APIResponse(
            success=True,
            message="Đã xóa nhà hàng thành công",
            data={"restaurant_id": restaurant.id}
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xóa nhà hàng: {str(e)}"
        )


# ================================
# Dashboard Endpoints
# ================================

@router.get("/dashboard/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Lấy tổng quan dashboard cho chủ nhà hàng"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Get rating details
        rating_details = db.query(RatingDetail).filter(
            RatingDetail.restaurant_id == restaurant.id
        ).first()

        # Get recent reviews (5 cái mới nhất)
        recent_reviews = db.query(Review).filter(
            Review.restaurant_id == restaurant.id
        ).order_by(Review.created_at.desc()).limit(5).all()

        # Get analytics data
        from datetime import datetime, timedelta
        last_week = datetime.now() - timedelta(days=7)

        weekly_analytics = db.query(RestaurantAnalytics).filter(
            RestaurantAnalytics.restaurant_id == restaurant.id,
            RestaurantAnalytics.date >= last_week
        ).all()

        # Calculate totals
        total_views = sum(a.page_views for a in weekly_analytics)
        total_visitors = sum(a.unique_visitors for a in weekly_analytics)
        weekly_reviews_count = len([r for r in recent_reviews if r.created_at >= last_week])

        # Extract top keywords
        all_keywords = {}
        for analytics in weekly_analytics:
            if analytics.top_keywords:
                for keyword, count in analytics.top_keywords.items():
                    all_keywords[keyword] = all_keywords.get(keyword, 0) + count

        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        top_keywords_list = [k[0] for k in top_keywords]

        dashboard_data = DashboardOverview(
            restaurant=RestaurantResponse.from_orm(restaurant),
            rating_summary=rating_details,
            total_page_views=total_views,
            total_unique_visitors=total_visitors,
            avg_rating=rating_details.overall_rating if rating_details else 0,
            total_reviews=rating_details.total_reviews if rating_details else 0,
            weekly_views=total_views,
            weekly_reviews=weekly_reviews_count,
            top_search_keywords=top_keywords_list,
            recent_reviews=[ReviewResponse.from_orm(r) for r in recent_reviews]
        )

        return dashboard_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy dashboard overview: {str(e)}"
        )


@router.get("/dashboard/analytics", response_model=AnalyticsData)
async def get_restaurant_analytics(
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """Lấy dữ liệu analytics chi tiết"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Parse dates
        from datetime import datetime, timedelta

        if date_from:
            start_date = datetime.strptime(date_from, "%Y-%m-%d")
        else:
            start_date = datetime.now() - timedelta(days=30)

        if date_to:
            end_date = datetime.strptime(date_to, "%Y-%m-%d")
        else:
            end_date = datetime.now()

        # Get analytics data
        analytics_records = db.query(RestaurantAnalytics).filter(
            RestaurantAnalytics.restaurant_id == restaurant.id,
            RestaurantAnalytics.date.between(start_date, end_date)
        ).order_by(RestaurantAnalytics.date).all()

        # Process data for charts
        daily_views = []
        search_keywords = {}
        total_sessions = 0
        total_bounce = 0
        total_ctr = 0

        for record in analytics_records:
            daily_views.append({
                "date": record.date.strftime("%Y-%m-%d"),
                "views": record.page_views,
                "visitors": record.unique_visitors,
                "impressions": record.search_impressions
            })

            # Aggregate keywords
            if record.top_keywords:
                for keyword, count in record.top_keywords.items():
                    search_keywords[keyword] = search_keywords.get(keyword, 0) + count

            total_sessions += record.unique_visitors
            total_bounce += record.bounce_rate * record.unique_visitors if record.bounce_rate else 0
            total_ctr += record.click_through_rate if record.click_through_rate else 0

        # Calculate averages
        avg_bounce_rate = (total_bounce / total_sessions) if total_sessions > 0 else 0
        avg_ctr = (total_ctr / len(analytics_records)) if analytics_records else 0
        avg_session_duration = sum(r.avg_time_on_page or 0 for r in analytics_records) / len(
            analytics_records) if analytics_records else 0

        # Top keywords list
        top_keywords = sorted(search_keywords.items(), key=lambda x: x[1], reverse=True)[:20]
        search_keywords_list = [{"keyword": k, "count": v} for k, v in top_keywords]

        analytics_data = AnalyticsData(
            restaurant_id=restaurant.id,
            date_range={
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            },
            daily_views=daily_views,
            visitor_demographics={
                "total_visitors": total_sessions,
                "returning_visitors": int(total_sessions * 0.3),  # Mock data
                "new_visitors": int(total_sessions * 0.7)  # Mock data
            },
            search_keywords=search_keywords_list,
            search_rankings={
                "average_position": 15,  # Mock data
                "top_10_keywords": 3,
                "total_keywords": len(search_keywords)
            },
            avg_session_duration=avg_session_duration,
            bounce_rate=avg_bounce_rate,
            click_through_rate=avg_ctr
        )

        return analytics_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy analytics: {str(e)}"
        )


# ================================
# Public Restaurant Endpoints
# ================================

@router.get("/", response_model=PaginatedResponse)
async def get_restaurants_list(
        page: int = 1,
        size: int = 10,
        cuisine_type: Optional[str] = None,
        province: Optional[str] = None,
        price_range: Optional[str] = None,
        min_rating: Optional[float] = None,
        search: Optional[str] = None,
        sort_by: str = "rating",
        sort_order: str = "desc",
        db: Session = Depends(get_db)
):
    """Lấy danh sách nhà hàng với filter và phân trang"""
    try:
        query = db.query(Restaurant).filter(Restaurant.status == "active")

        # Apply filters
        if cuisine_type:
            query = query.filter(Restaurant.cuisine_type == cuisine_type)

        if province:
            query = query.filter(Restaurant.province == province)

        if price_range:
            query = query.filter(Restaurant.price_range == price_range)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Restaurant.name.ilike(search_term) |
                Restaurant.description.ilike(search_term) |
                Restaurant.ai_enhanced_description.ilike(search_term)
            )

        # Join with rating for filtering by rating
        if min_rating:
            query = query.join(RatingDetail).filter(
                RatingDetail.overall_rating >= min_rating
            )

        # Apply sorting
        if sort_by == "rating":
            query = query.join(RatingDetail).order_by(
                RatingDetail.overall_rating.desc() if sort_order == "desc"
                else RatingDetail.overall_rating.asc()
            )
        elif sort_by == "newest":
            query = query.order_by(
                Restaurant.created_at.desc() if sort_order == "desc"
                else Restaurant.created_at.asc()
            )
        elif sort_by == "name":
            query = query.order_by(
                Restaurant.name.desc() if sort_order == "desc"
                else Restaurant.name.asc()
            )

        # Paginate results
        paginated_result = paginate(query, page, size)

        return PaginatedResponse(
            items=[RestaurantListResponse.from_orm(r) for r in paginated_result.items],
            total=paginated_result.total,
            page=page,
            size=size,
            pages=paginated_result.pages
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy danh sách nhà hàng: {str(e)}"
        )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant_detail(
        restaurant_id: int,
        db: Session = Depends(get_db)
):
    """Lấy chi tiết một nhà hàng"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.id == restaurant_id,
            Restaurant.status == "active"
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Increment page view counter
        today = datetime.now().date()
        analytics_record = db.query(RestaurantAnalytics).filter(
            RestaurantAnalytics.restaurant_id == restaurant_id,
            RestaurantAnalytics.date == today
        ).first()

        if analytics_record:
            analytics_record.page_views += 1
        else:
            new_analytics = RestaurantAnalytics(
                restaurant_id=restaurant_id,
                date=today,
                page_views=1,
                unique_visitors=1,
                search_impressions=0
            )
            db.add(new_analytics)

        db.commit()

        return RestaurantResponse.from_orm(restaurant)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy chi tiết nhà hàng: {str(e)}"
        )


# ================================
# AI Suggestion Endpoints
# ================================

@router.post("/suggest-improvements", response_model=APIResponse)
async def get_improvement_suggestions(
        current_user: User = Depends(require_role("restaurant_owner")),
        db: Session = Depends(get_db)
):
    """AI gợi ý cải thiện nhà hàng"""
    try:
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy nhà hàng"
            )

        # Convert restaurant to request format for AI analysis
        restaurant_data = RestaurantCreateRequest(
            name=restaurant.name,
            description=restaurant.description,
            cuisine_type=restaurant.cuisine_type,
            address=restaurant.address,
            province=restaurant.province,
            district=restaurant.district,
            ward=restaurant.ward,
            logo_url=restaurant.logo_url,
            cover_image_url=restaurant.cover_image_url,
            gallery_images=restaurant.gallery_images or [],
            opening_hours=restaurant.opening_hours or {},
            price_range=restaurant.price_range,
            facilities=restaurant.facilities or []
        )

        suggestions = await ai_service.suggest_improvements(restaurant_data)

        return APIResponse(
            success=True,
            message="Đã tạo gợi ý cải thiện",
            data={"suggestions": suggestions}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo gợi ý cải thiện: {str(e)}"
        )


# ================================
# Statistics Endpoints
# ================================

@router.get("/stats/summary", response_model=APIResponse)
async def get_restaurant_stats():
    """Thống kê tổng quan hệ thống nhà hàng"""
    try:
        # Mock data - thay thế bằng query thực tế
        stats = {
            "total_restaurants": 150,
            "by_cuisine": {
                "Việt Nam": 45,
                "Nhật Bản": 25,
                "Hàn Quốc": 20,
                "Trung Hoa": 18,
                "Thái Lan": 12,
                "Âu": 10,
                "Khác": 20
            },
            "by_province": {
                "TP.HCM": 60,
                "Hà Nội": 35,
                "Đà Nẵng": 15,
                "Gia Lai": 25,
                "Khác": 15
            },
            "by_price_range": {
                "cheap": 45,
                "medium": 78,
                "expensive": 27
            },
            "average_rating": 4.2
        }

        return APIResponse(
            success=True,
            message="Thống kê hệ thống",
            data=stats
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy thống kê: {str(e)}"
        )