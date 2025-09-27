#!/usr/bin/env python3
"""
Setup đơn giản chỉ tạo database và tables
Bỏ qua LLM để tránh lỗi import
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test import các module cần thiết"""
    print("🧪 Kiểm tra imports...")

    try:
        from database import engine, SessionLocal, test_connection
        print("✅ Database module OK")
    except ImportError as e:
        print(f"❌ Database module failed: {e}")
        return False

    try:
        import models
        print("✅ Models module OK")
    except ImportError as e:
        print(f"❌ Models module failed: {e}")
        return False

    try:
        import schemas
        print("✅ Schemas module OK")
    except ImportError as e:
        print(f"❌ Schemas module failed: {e}")
        return False

    return True


def create_tables():
    """Tạo các bảng database"""
    print("🔨 Tạo bảng database...")

    try:
        import models
        from database import engine

        models.Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo thành công các bảng!")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo bảng: {e}")
        return False


def create_sample_users():
    """Tạo user mẫu đơn giản"""
    print("👤 Tạo user mẫu...")

    try:
        from database import SessionLocal
        import models

        db = SessionLocal()

        # Check if admin user exists
        existing_admin = db.query(models.User).filter(
            models.User.username == "admin"
        ).first()

        if not existing_admin:
            admin_user = models.User(
                username="admin",
                email="admin@restaurant.com",
                full_name="Administrator",
                phone="0901234567",
                hashed_password="hashed_password_123",  # In production, hash properly
                is_restaurant_owner=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Đã tạo admin user")
        else:
            print("👤 Admin user đã tồn tại")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Lỗi tạo user: {e}")
        return False


def create_sample_restaurant():
    """Tạo nhà hàng mẫu"""
    print("🏪 Tạo nhà hàng mẫu...")

    try:
        from database import SessionLocal
        import models

        db = SessionLocal()

        # Get admin user
        admin_user = db.query(models.User).filter(
            models.User.username == "admin"
        ).first()

        if not admin_user:
            print("❌ Không tìm thấy admin user")
            return False

        # Check if restaurant exists
        existing_restaurant = db.query(models.Restaurant).filter(
            models.Restaurant.name == "Phở Hà Nội"
        ).first()

        if not existing_restaurant:
            sample_restaurant = models.Restaurant(
                name="Phở Hà Nội",
                description="Quán phở truyền thống với hương vị đặc trưng Hà Nội",
                category="Vietnamese",
                address="123 Nguyễn Huệ, Quận 1, TP.HCM",
                phone="0281234567",
                email="pho.hanoi@gmail.com",
                price_range="budget",
                average_price=50000,
                features=["wifi", "air_conditioning", "takeout"],
                cuisine_types=["Vietnamese", "Noodles"],
                business_hours={
                    "monday": "06:00-22:00",
                    "tuesday": "06:00-22:00",
                    "wednesday": "06:00-22:00",
                    "thursday": "06:00-22:00",
                    "friday": "06:00-22:00",
                    "saturday": "06:00-23:00",
                    "sunday": "06:00-23:00"
                },
                owner_id=admin_user.id,
                is_active=True,
                is_verified=True
            )

            db.add(sample_restaurant)
            db.commit()
            print("✅ Đã tạo nhà hàng Phở Hà Nội")
        else:
            print("🏪 Nhà hàng mẫu đã tồn tại")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Lỗi tạo nhà hàng: {e}")
        return False


def print_completion_info():
    """In thông tin hoàn thành setup"""
    print("\n" + "=" * 60)
    print("🎉 SETUP CƠ BẢN HOÀN THÀNH!")
    print("=" * 60)

    print("\n✅ Đã hoàn thành:")
    print("   • Tạo bảng database")
    print("   • Tạo user admin")
    print("   • Tạo nhà hàng mẫu")

    print("\n🚀 Chạy ứng dụng:")
    print("   python main_simple.py")
    print("   # hoặc")
    print("   python main.py")

    print("\n🌐 Truy cập:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")

    print("\n💡 Test API endpoints:")
    print("   • GET /restaurants/ - Xem nhà hàng")
    print("   • GET /health - Kiểm tra trạng thái")

    print("\n🤖 Để setup LLM:")
    print("   1. Cài đặt Ollama")
    print("   2. Chạy: ollama pull llama3.2:3b")
    print("   3. Test: ollama list")
    print("=" * 60)


def main():
    """Main setup function"""
    print("🎯 RESTAURANT COMMUNITY - SIMPLE SETUP")
    print("=" * 50)

    # 1. Test imports
    print("\n1️⃣ Kiểm tra imports...")
    if not test_imports():
        print("❌ Import failed! Hãy kiểm tra các file đã tạo đúng chưa")
        return False

    # 2. Test database connection
    print("\n2️⃣ Kiểm tra database connection...")
    try:
        # Import function mới
        from database import test_connection_detailed
        if not test_connection_detailed():
            print("❌ Không thể kết nối database!")
            return False
    except ImportError:
        # Fallback to basic test
        try:
            from database import test_connection
            if not test_connection():
                print("❌ Không thể kết nối database!")
                return False
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

    # 3. Create tables
    print("\n3️⃣ Tạo bảng...")
    if not create_tables():
        return False

    # 4. Create sample data
    print("\n4️⃣ Tạo dữ liệu mẫu...")
    if not create_sample_users():
        print("⚠️  Không tạo được user mẫu")

    if not create_sample_restaurant():
        print("⚠️  Không tạo được nhà hàng mẫu")

    # 5. Success message
    print_completion_info()

    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Setup thành công!")
            sys.exit(0)
        else:
            print("\n💥 Setup thất bại!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup bị hủy")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Lỗi không mong muốn: {e}")
        sys.exit(1)