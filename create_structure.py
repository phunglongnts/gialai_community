#!/usr/bin/env python3
"""
Script tạo cấu trúc thư mục cho Restaurant Community project
Chạy script này TRƯỚC khi chạy setup.py
"""

import os
import sys


def create_directories():
    """Tạo các thư mục cần thiết"""
    directories = [
        'services',
        'logs',
        'uploads',
        'tests'
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Đã tạo thư mục: {directory}/")
        else:
            print(f"📁 Thư mục đã tồn tại: {directory}/")


def create_init_files():
    """Tạo các __init__.py files"""
    init_files = [
        'services/__init__.py',
        'tests/__init__.py'
    ]

    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                if 'services' in init_file:
                    f.write('"""Services package"""\n')
                    f.write('from .restaurant_service import RestaurantService\n')
                    f.write('from .llm_service import LLMService\n')
                    f.write('__all__ = ["RestaurantService", "LLMService"]\n')
                else:
                    f.write('"""Tests package"""\n')
            print(f"✅ Đã tạo: {init_file}")
        else:
            print(f"📄 File đã tồn tại: {init_file}")


def create_env_file():
    """Tạo .env file từ template"""
    if not os.path.exists('.env'):
        env_content = """# Database Configuration
DATABASE_URL=postgresql://postgres:123456@localhost:5432/restaurant_community
DB_HOST=localhost
DB_PORT=5432
DB_NAME=restaurant_community
DB_USER=postgres
DB_PASSWORD=123456

# Application Settings
APP_NAME=Restaurant Community API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3.2:3b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Security
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Đã tạo file .env")
    else:
        print("📄 File .env đã tồn tại")


def check_required_files():
    """Kiểm tra các file cần thiết"""
    required_files = [
        'main.py',
        'database_old.py',
        'models.py',
        'schemas.py',
        'services/restaurant_service.py',
        'services/llm_service.py',
        'requirements_minimal.txt'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"\n❌ Các file còn thiếu:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False

    print(f"\n🎉 Tất cả files cần thiết đã có!")
    return True


def main():
    """Tạo cấu trúc project hoàn chỉnh"""
    print("🏗️  TẠO CẤU TRÚC RESTAURANT COMMUNITY PROJECT")
    print("=" * 60)

    print("\n1️⃣ Tạo thư mục...")
    create_directories()

    print("\n2️⃣ Tạo __init__.py files...")
    create_init_files()

    print("\n3️⃣ Tạo .env file...")
    create_env_file()

    print("\n4️⃣ Kiểm tra files cần thiết...")
    all_files_exist = check_required_files()

    if all_files_exist:
        print("\n" + "=" * 60)
        print("🎉 CẤU TRÚC PROJECT ĐÃ HOÀN THÀNH!")
        print("\n📋 Cấu trúc cuối cùng:")
        print("""
restaurant_community/
├── main.py
├── database_old.py
├── models.py
├── schemas.py  
├── setup.py
├── .env
├── requirements_minimal.txt
├── services/
│   ├── __init__.py
│   ├── restaurant_service.py
│   └── llm_service.py
├── logs/
├── uploads/
└── tests/
    └── __init__.py
        """)
        print("🚀 Bây giờ bạn có thể chạy:")
        print("   python setup.py")
        return True
    else:
        print("\n❌ Vẫn còn thiếu một số files!")
        print("💡 Hãy tạo các files còn thiếu từ artifacts trước")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Lỗi: {e}")
        sys.exit(1)