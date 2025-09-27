#!/usr/bin/env python3
"""
Setup script cho Restaurant Community Project
Chạy script này để thiết lập database và dữ liệu mẫu
"""

import asyncio
import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import với error handling
try:
    from database import engine, SessionLocal, test_connection_detailed
    import models
    import schemas
    from services.restaurant_service import RestaurantService
    from services.llm_service import LLMService
except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    print("💡 Hãy đảm bảo tất cả files đã được tạo đúng cấu trúc!")
    sys.exit(1)


def create_tables():
    """Tạo các bảng trong database"""
    print("🔨 Tạo bảng database...")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo thành công các bảng!")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo bảng: {e}")
        return False


def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("📝 Tạo dữ liệu mẫu...")

    db = SessionLocal()
    restaurant_service = RestaurantService()

    try:
        # Sample users
        sample_users = [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@restaurant.com",
                "full_name": "Quản trị viên",
                "phone": "0901234567",
                "hashed_password": "hashed_password_here",  # In production, hash properly
                "is_restaurant_owner": True
            },
            {
                "id": 2,
                "username": "user1",
                "email": "user1@gmail.com",
                "full_name": "Nguyễn Văn A",
                "phone": "0901234568",
                "hashed_password": "hashed_password_here",
                "is_restaurant_owner": False
            }
        ]

        for user_data in sample_users:
            existing_user = db.query(models.User).filter(
                models.User.username == user_data["username"]
            ).first()

            if not existing_user:
                user = models.User(**user_data)
                db.add(user)

        db.commit()
        print("✅ Đã tạo người dùng mẫu!")

        # Sample restaurants
        sample_restaurants = [
            {
                "name": "Phở Hà Nội",
                "description": "Quán phở truyền thống với hương vị đặc trưng của Hà Nội. Nước dùng trong, thịt bò tươi ngon.",
                "category": "Vietnamese",
                "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
                "phone": "0281234567",
                "email": "pho.hanoi@gmail.com",
                "price_range": "budget",
                "average_price": 50000,
                "features": ["wifi", "air_conditioning", "takeout"],
                "cuisine_types": ["Vietnamese", "Noodles"],
                "business_hours": {
                    "monday": "06:00-22:00",
                    "tuesday": "06:00-22:00",
                    "wednesday": "06:00-22:00",
                    "thursday": "06:00-22:00",
                    "friday": "06:00-22:00",
                    "saturday": "06:00-23:00",
                    "sunday": "06:00-23:00"
                },
                "owner_id": 1
            },
            {
                "name": "Sushi Sakura",
                "description": "Nhà hàng Nhật Bản cao cấp với sushi tươi ngon và không gian sang trọng.",
                "category": "Japanese",
                "address": "456 Lê Lợi, Quận 3, TP.HCM",
                "phone": "0281234568",
                "email": "sakura@sushi.com",
                "price_range": "high-end",
                "average_price": 300000,
                "features": ["wifi", "air_conditioning", "parking", "romantic"],
                "cuisine_types": ["Japanese", "Sushi", "Sashimi"],
                "business_hours": {
                    "monday": "11:00-14:00,17:00-22:00",
                    "tuesday": "11:00-14:00,17:00-22:00",
                    "wednesday": "11:00-14:00,17:00-22:00",
                    "thursday": "11:00-14:00,17:00-22:00",
                    "friday": "11:00-14:00,17:00-23:00",
                    "saturday": "11:00-23:00",
                    "sunday": "11:00-22:00"
                },
                "owner_id": 1
            },
            {
                "name": "Pizza Italia",
                "description": "Pizza Ý chính hiệu với lò nướng đá và nguyên liệu nhập khẩu từ Italia.",
                "category": "Italian",
                "address": "789 Điện Biên Phủ, Quận Bình Thạnh, TP.HCM",
                "phone": "0281234569",
                "email": "pizza@italia.com",
                "price_range": "mid-range",
                "average_price": 150000,
                "features": ["wifi", "delivery", "family-friendly", "outdoor-seating"],
                "cuisine_types": ["Italian", "Pizza", "Pasta"],
                "business_hours": {
                    "monday": "10:00-23:00",
                    "tuesday": "10:00-23:00",
                    "wednesday": "10:00-23:00",
                    "thursday": "10:00-23:00",
                    "friday": "10:00-24:00",
                    "saturday": "10:00-24:00",
                    "sunday": "10:00-23:00"
                },
                "owner_id": 1
            },
            {
                "name": "Cơm Tấm Sài Gòn",
                "description": "Cơm tấm truyền thống Sài Gòn với sườn nướng thơm phức và nước mắm pha đặc biệt.",
                "category": "Vietnamese",
                "address": "321 Võ Văn Tần, Quận 10, TP.HCM",
                "phone": "0281234570",
                "price_range": "budget",
                "average_price": 45000,
                "features": ["takeout", "delivery", "budget-friendly"],
                "cuisine_types": ["Vietnamese", "Rice", "Grilled"],
                "business_hours": {
                    "monday": "06:00-21:00",
                    "tuesday": "06:00-21:00",
                    "wednesday": "06:00-21:00",
                    "thursday": "06:00-21:00",
                    "friday": "06:00-21:00",
                    "saturday": "06:00-21:00",
                    "sunday": "06:00-21:00"
                },
                "owner_id": 1
            },
            {
                "name": "Café Arabica",
                "description": "Quán cà phê specialty với hạt cà phê rang xay tươi và không gian cozy.",
                "category": "Cafe",
                "address": "654 Nguyễn Trãi, Quận 5, TP.HCM",
                "phone": "0281234571",
                "email": "info@arabica.coffee",
                "price_range": "mid-range",
                "average_price": 80000,
                "features": ["wifi", "air_conditioning", "study-friendly", "instagram-worthy"],
                "cuisine_types": ["Coffee", "Dessert", "Light meals"],
                "business_hours": {
                    "monday": "07:00-22:00",
                    "tuesday": "07:00-22:00",
                    "wednesday": "07:00-22:00",
                    "thursday": "07:00-22:00",
                    "friday": "07:00-23:00",
                    "saturday": "08:00-23:00",
                    "sunday": "08:00-22:00"
                },
                "owner_id": 1
            }
        ]

        created_restaurants = []
        for restaurant_data in sample_restaurants:
            existing = db.query(models.Restaurant).filter(
                models.Restaurant.name == restaurant_data["name"]
            ).first()

            if not existing:
                restaurant_create = schemas.RestaurantCreate(**restaurant_data)
                restaurant = restaurant_service.create_restaurant(db, restaurant_create)
                created_restaurants.append(restaurant)
                print(f"✅ Đã tạo nhà hàng: {restaurant.name}")

        # Sample reviews
        if created_restaurants:
            sample_reviews = [
                {
                    "restaurant_id": created_restaurants[0].id,  # Phở Hà Nội
                    "user_id": 2,
                    "rating": 5,
                    "title": "Phở rất ngon!",
                    "content": "Nước dùng trong vắt, thịt bò mềm, bánh phở dai ngon. Giá cả hợp lý, phục vụ nhiệt tình. Sẽ quay lại!",
                    "food_rating": 5,
                    "service_rating": 4,
                    "ambiance_rating": 4,
                    "value_rating": 5,
                    "visit_type": "dine-in",
                    "party_size": 2
                },
                {
                    "restaurant_id": created_restaurants[1].id if len(created_restaurants) > 1 else created_restaurants[
                        0].id,  # Sushi Sakura
                    "user_id": 2,
                    "rating": 4,
                    "title": "Sushi tươi ngon",
                    "content": "Cá hồi tươi, sushi cuộn đẹp mắt. Không gian sang trọng nhưng giá hơi cao. Phù hợp cho dịp đặc biệt.",
                    "food_rating": 5,
                    "service_rating": 4,
                    "ambiance_rating": 5,
                    "value_rating": 3,
                    "visit_type": "dine-in",
                    "party_size": 4
                }
            ]

            for review_data in sample_reviews:
                review_create = schemas.ReviewCreate(**review_data)
                restaurant_service.create_review(db, review_create)

            print("✅ Đã tạo đánh giá mẫu!")

        print("🎉 Hoàn thành tạo dữ liệu mẫu!")
        return True

    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi tạo dữ liệu mẫu: {e}")
        return False
    finally:
        db.close()


async def test_llm_connection():
    """Test kết nối với LLM"""
    print("🤖 Kiểm tra kết nối LLM...")

    llm_service = LLMService()
    try:
        status = await llm_service.health_check()
        if "OK" in status:
            print("✅ LLM kết nối thành công!")

            # Test simple query
            test_response = await llm_service.generate_response(
                "Chào bạn! Tôi là AI hỗ trợ tìm kiếm nhà hàng.",
                "Bạn là trợ lý AI thân thiện."
            )
            print(f"🧪 Test response: {test_response[:100]}...")
            return True
        else:
            print(f"❌ LLM có vấn đề: {status}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kết nối LLM: {e}")
        print("💡 Hãy chắc chắn rằng Ollama đang chạy và đã tải model llama3.2:3b")
        return False
    finally:
        await llm_service.close()


def print_setup_info():
    """In thông tin thiết lập"""
    print("\n" + "=" * 60)
    print("🏪 RESTAURANT COMMUNITY - SETUP HOÀN TẤT")
    print("=" * 60)
    print("📋 Thông tin hệ thống:")
    print("   • Database: PostgreSQL")
    print("   • API Framework: FastAPI")
    print("   • LLM: Llama 3.2 3B (qua Ollama)")
    print("   • Port: 8000")
    print("\n🚀 Để chạy ứng dụng:")
    print("   python main.py")
    print("   hoặc: uvicorn main:app --reload")
    print("\n🌐 Truy cập:")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("\n📝 API endpoints chính:")
    print("   • GET /restaurants/ - Danh sách nhà hàng")
    print("   • POST /ai/search - Tìm kiếm với AI")
    print("   • POST /ai/chat - Chat với AI")
    print("   • POST /restaurants/ - Tạo nhà hàng mới")
    print("   • POST /reviews/ - Tạo đánh giá")
    print("\n💡 Tips:")
    print("   • Xem file .env.example để cấu hình")
    print("   • Chạy 'ollama list' để kiểm tra models")
    print("   • Dùng pgAdmin4 để quản lý database")
    print("=" * 60)


async def main():
    """Hàm chính setup"""
    print("🎯 KHỞI ĐỘNG SETUP RESTAURANT COMMUNITY")
    print("=" * 50)

    # 1. Test database connection
    print("\n1️⃣ Kiểm tra kết nối PostgreSQL...")
    if not test_connection_detailed():
        print("❌ Không thể kết nối PostgreSQL!")
        print("💡 Hãy kiểm tra:")
        print("   • PostgreSQL đang chạy")
        print("   • Thông tin kết nối trong .env")
        print("   • Database đã được tạo")
        return False

    # 2. Create tables
    print("\n2️⃣ Tạo bảng database...")
    if not create_tables():
        return False

    # 3. Test LLM
    print("\n3️⃣ Kiểm tra LLM...")
    llm_ok = await test_llm_connection()
    if not llm_ok:
        print("⚠️  LLM chưa sẵn sàng, nhưng có thể tiếp tục setup")

    # 4. Create sample data
    print("\n4️⃣ Tạo dữ liệu mẫu...")
    if not create_sample_data():
        print("⚠️  Không tạo được dữ liệu mẫu, nhưng setup cơ bản đã hoàn thành")

    # 5. Print info
    print_setup_info()

    print("\n✨ Setup hoàn tất! Hãy chạy ứng dụng và test thử.")
    return True


if __name__ == "__main__":
    # Chạy setup
    try:
        result = asyncio.run(main())
        if result:
            print("\n🎉 Setup thành công!")
            sys.exit(0)
        else:
            print("\n💥 Setup thất bại!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Lỗi không mong muốn: {e}")
        sys.exit(1)