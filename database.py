from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - Thay đổi thông tin này theo PostgreSQL của bạn
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/restaurant_community"
)

print(f"🔗 Connecting to: {DATABASE_URL}")

# Tạo engine với SQLAlchemy 2.0 compatible settings
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    # SQLAlchemy 2.0 compatibility
    future=True
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho models
Base = declarative_base()


# Dependency để lấy database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Kiểm tra kết nối database với SQLAlchemy 2.0 syntax
def test_connection():
    try:
        db = SessionLocal()
        # SQLAlchemy 2.0 requires text() for raw SQL
        result = db.execute(text("SELECT 1"))
        db.close()
        print("✅ Kết nối PostgreSQL thành công!")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối PostgreSQL: {e}")
        return False


# Test connection với thông tin chi tiết
def test_connection_detailed():
    try:
        print("🔍 Testing database connection...")
        print(f"📍 URL: {DATABASE_URL}")

        # Test tạo engine
        test_engine = create_engine(DATABASE_URL, echo=False)

        # Test connection
        with test_engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"🐘 PostgreSQL version: {version[:50]}...")

        # Test session
        db = SessionLocal()
        db.execute(text("SELECT current_database()"))
        db.close()

        print("✅ Database connection successful!")
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")

        # Detailed error info
        if "could not connect to server" in str(e).lower():
            print("💡 PostgreSQL server không chạy hoặc không thể kết nối")
            print("   - Kiểm tra PostgreSQL service")
            print("   - Kiểm tra host/port trong DATABASE_URL")
        elif "authentication failed" in str(e).lower():
            print("💡 Sai username/password")
            print("   - Kiểm tra credentials trong DATABASE_URL")
        elif "database" in str(e).lower() and "does not exist" in str(e).lower():
            print("💡 Database chưa được tạo")
            print("   - Tạo database 'restaurant_community' trong pgAdmin4")

        return False


if __name__ == "__main__":
    test_connection_detailed()