#!/usr/bin/env python3
"""
Phase 2 Setup Script - Authentication System Integration
"""

import sys
import os
import subprocess
import shutil
from datetime import datetime


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"🚀 {text}")
    print('=' * 60)


def print_step(step, text):
    print(f"\n{step}️⃣  {text}")


def run_command(command, description=""):
    """Run command and return success status"""
    try:
        print(f"   Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr.strip()}")
        return False


def check_requirements():
    """Check if all required files exist"""
    print_step(1, "Kiểm tra requirements...")

    required_files = [
        'database.py',
        'models.py',
        'schemas.py',
        'services/restaurant_service.py',
        'services/llm_service.py',
        '.env'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   ✅ {file}")

    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        print("   Please create these files from the artifacts first!")
        return False

    print("   ✅ All required files present!")
    return True


def backup_existing_files():
    """Backup existing files before updating"""
    print_step(2, "Backup files hiện tại...")

    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    files_to_backup = [
        'main.py',
        'requirements.txt'
    ]

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"   📁 Created backup directory: {backup_dir}")

    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(backup_dir, file))
            print(f"   💾 Backed up: {file}")

    print(f"   ✅ Backup completed in {backup_dir}/")
    return backup_dir


def install_auth_dependencies():
    """Install authentication dependencies"""
    print_step(3, "Cài đặt authentication dependencies...")

    auth_packages = [
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6"
    ]

    success = True
    for package in auth_packages:
        print(f"   Installing {package}...")
        if not run_command(f"pip install {package}"):
            success = False

    if success:
        print("   ✅ All authentication packages installed!")
    else:
        print("   ❌ Some packages failed to install")

    return success


def create_auth_files():
    """Create authentication system files"""
    print_step(4, "Tạo authentication system files...")

    # Create routes directory
    if not os.path.exists('routes'):
        os.makedirs('routes')
        print("   📁 Created routes/ directory")

    # Create __init__.py for routes
    with open('routes/__init__.py', 'w') as f:
        f.write('"""Routes package"""\n')
    print("   📄 Created routes/__init__.py")

    files_created = []

    # Files to create (would be copied from artifacts in real implementation)
    required_auth_files = [
        'auth.py',
        'routes/auth.py'
    ]

    for file in required_auth_files:
        if not os.path.exists(file):
            print(f"   ⚠️  Need to create: {file}")
            print(f"      Copy content from corresponding artifact")
            files_created.append(file)

    if files_created:
        print("   📋 Files that need to be created from artifacts:")
        for file in files_created:
            print(f"      - {file}")
        return False

    print("   ✅ Authentication files ready!")
    return True


def update_env_file():
    """Update .env file with auth settings"""
    print_step(5, "Cập nhật .env file...")

    auth_vars = [
        "# Authentication Settings",
        "JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-please",
        "JWT_ALGORITHM=HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES=30",
        "REFRESH_TOKEN_EXPIRE_DAYS=7",
        ""
    ]

    try:
        # Check if auth vars already exist
        with open('.env', 'r') as f:
            content = f.read()

        if 'JWT_SECRET_KEY' in content:
            print("   ℹ️  Authentication settings already exist in .env")
            return True

        # Append auth settings
        with open('.env', 'a') as f:
            f.write('\n')
            for line in auth_vars:
                f.write(line + '\n')

        print("   ✅ Added authentication settings to .env")
        return True

    except Exception as e:
        print(f"   ❌ Error updating .env: {e}")
        return False


def update_database_schema():
    """Update database schema for authentication"""
    print_step(6, "Cập nhật database schema...")

    try:
        # Import và tạo tables mới
        print("   📊 Updating database tables...")

        # This would typically run Alembic migrations
        # For now, we'll recreate tables
        from database import engine
        import models

        print("   🔨 Creating/updating tables...")
        models.Base.metadata.create_all(bind=engine)

        print("   ✅ Database schema updated successfully!")
        return True

    except Exception as e:
        print(f"   ❌ Database update error: {e}")
        return False


def create_admin_user():
    """Create default admin user"""
    print_step(7, "Tạo admin user mặc định...")

    try:
        from database import SessionLocal
        import models
        from auth import get_password_hash

        db = SessionLocal()

        # Check if admin exists
        existing_admin = db.query(models.User).filter(
            models.User.username == "admin"
        ).first()

        if existing_admin:
            print("   ℹ️  Admin user already exists")
            db.close()
            return True

        # Create admin user
        admin_user = models.User(
            username="admin",
            email="admin@restaurant.com",
            full_name="System Administrator",
            phone="0901234567",
            hashed_password=get_password_hash("admin123456"),
            is_restaurant_owner=True,
            is_active=True
        )

        db.add(admin_user)
        db.commit()

        print("   ✅ Admin user created successfully!")
        print("   📋 Login credentials:")
        print("      Username: admin")
        print("      Password: admin123456")
        print("      ⚠️  Please change password after first login!")

        db.close()
        return True

    except Exception as e:
        print(f"   ❌ Admin user creation error: {e}")
        return False


def test_authentication():
    """Test authentication system"""
    print_step(8, "Test authentication system...")

    try:
        # Test password hashing
        from auth import get_password_hash, verify_password

        test_password = "test123"
        hashed = get_password_hash(test_password)

        if verify_password(test_password, hashed):
            print("   ✅ Password hashing works!")
        else:
            print("   ❌ Password hashing failed!")
            return False

        # Test JWT token creation
        from auth import create_access_token
        from datetime import timedelta

        token = create_access_token(
            data={"sub": "testuser", "user_id": 1},
            expires_delta=timedelta(minutes=5)
        )

        if token:
            print("   ✅ JWT token creation works!")
            print(f"   🔑 Sample token: {token[:50]}...")
        else:
            print("   ❌ JWT token creation failed!")
            return False

        print("   ✅ Authentication system test passed!")
        return True

    except Exception as e:
        print(f"   ❌ Authentication test error: {e}")
        return False


def display_next_steps():
    """Display next steps for user"""
    print_step(9, "Các bước tiếp theo...")

    steps = [
        "1. Copy authentication files from artifacts:",
        "   - auth.py (main authentication module)",
        "   - routes/auth.py (authentication API routes)",
        "   - main_with_auth.py → main.py (updated main file)",
        "",
        "2. Start the server:",
        "   python main.py",
        "",
        "3. Test authentication:",
        "   - Visit: http://localhost:8000/docs",
        "   - Try register/login endpoints",
        "   - Use frontend: auth_components.html",
        "",
        "4. Default admin login:",
        "   - Username: admin",
        "   - Password: admin123456",
        "   - Change password after first login!",
        "",
        "5. API endpoints available:",
        "   - POST /auth/register - User registration",
        "   - POST /auth/login - User login",
        "   - GET /auth/me - Get user profile",
        "   - POST /auth/logout - User logout",
        "   - Protected restaurant/review endpoints",
        "",
        "6. Frontend integration:",
        "   - Open auth_components.html in browser",
        "   - Test login/register functionality",
        "   - User authentication works with AI search",
        "",
        "7. Next features to implement:",
        "   - Image upload system",
        "   - Advanced review system",
        "   - Real-time notifications",
        "   - Analytics dashboard"
    ]

    for step in steps:
        print(f"   {step}")


def main():
    """Main setup function"""
    print_header("RESTAURANT COMMUNITY - PHASE 2 SETUP")
    print("🔐 Adding Authentication System")

    success_steps = 0
    total_steps = 8

    # Step 1: Check requirements
    if check_requirements():
        success_steps += 1
    else:
        print("\n💥 Setup failed at requirements check!")
        return False

    # Step 2: Backup existing files
    backup_dir = backup_existing_files()
    if backup_dir:
        success_steps += 1

    # Step 3: Install dependencies
    if install_auth_dependencies():
        success_steps += 1
    else:
        print("\n⚠️  Dependency installation had issues, but continuing...")

    # Step 4: Create auth files
    if create_auth_files():
        success_steps += 1
    else:
        print("\n⚠️  You need to manually create auth files from artifacts")

    # Step 5: Update .env
    if update_env_file():
        success_steps += 1

    # Step 6: Update database schema
    try:
        if update_database_schema():
            success_steps += 1
    except:
        print("   ⚠️  Database update will be done when you run the app")

    # Step 7: Create admin user
    try:
        if create_admin_user():
            success_steps += 1
    except:
        print("   ⚠️  Admin user will be created when auth system is ready")

    # Step 8: Test authentication
    try:
        if test_authentication():
            success_steps += 1
    except:
        print("   ⚠️  Authentication test will work after files are created")

    # Display results
    print_header("SETUP RESULTS")
    print(f"📊 Progress: {success_steps}/{total_steps} steps completed")

    if success_steps >= 6:
        print("🎉 SETUP MOSTLY SUCCESSFUL!")
        print("✨ Authentication system is ready to be integrated!")
    else:
        print("⚠️  SETUP PARTIALLY COMPLETED")
        print("🛠️  Some manual steps required")

    # Display next steps
    display_next_steps()

    print_header("PHASE 2 AUTHENTICATION SETUP COMPLETE")

    return success_steps >= 6


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Ready for Phase 2 development!")
            sys.exit(0)
        else:
            print("\n🔧 Manual completion required")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)