"""
Fixed Authentication API Routes - Handles hash and validation issues
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from database import get_db
import models
from auth import (
    UserRegister, UserLogin, Token, UserProfile,
    authenticate_user, create_user, get_current_user, get_current_active_user,
    generate_tokens, refresh_access_token, get_password_hash, verify_password,
    get_user_by_username, get_user_by_email
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user with enhanced validation
    """
    try:
        logger.info(f"Registration attempt for username: {user_data.username}")

        # Create new user
        user = create_user(db, user_data)

        # Generate tokens
        tokens = generate_tokens(user)

        logger.info(f"User registered successfully: {user.username} ({user.email})")

        return tokens

    except HTTPException as e:
        logger.error(f"Registration failed for {user_data.username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error"
        )

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user with enhanced error handling
    """
    try:
        logger.info(f"Login attempt for: {user_credentials.username_or_email}")

        # Authenticate user
        user = authenticate_user(db, user_credentials.username_or_email, user_credentials.password)

        if not user:
            logger.warning(f"Authentication failed for: {user_credentials.username_or_email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate tokens
        tokens = generate_tokens(user)

        logger.info(f"User logged in successfully: {user.username}")

        return tokens

    except HTTPException as e:
        logger.error(f"Login HTTP error for {user_credentials.username_or_email}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected login error for {user_credentials.username_or_email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error"
        )

@router.post("/login/form", response_model=Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible login endpoint
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        tokens = generate_tokens(user)
        return tokens

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Form login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    try:
        tokens = refresh_access_token(refresh_token, db)
        return tokens

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: models.User = Depends(get_current_active_user)):
    """
    Get current user's profile information
    """
    try:
        return UserProfile.from_orm(current_user)
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile retrieval failed"
        )

@router.put("/me", response_model=UserProfile)
async def update_user_profile(
    full_name: str = None,
    phone: str = None,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information
    """
    try:
        # Update user fields
        if full_name is not None and full_name.strip():
            current_user.full_name = full_name.strip()
        if phone is not None:
            current_user.phone = phone.strip() if phone.strip() else None

        current_user.updated_at = datetime.now()

        db.commit()
        db.refresh(current_user)

        logger.info(f"User profile updated: {current_user.username}")

        return UserProfile.from_orm(current_user)

    except Exception as e:
        db.rollback()
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user's password
    """
    try:
        # Validate input
        if not current_password or not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password and new password are required"
            )

        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long"
            )

        # Verify current password
        if not verify_password(current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        # Hash new password
        new_hashed_password = get_password_hash(new_password)

        # Update password
        current_user.hashed_password = new_hashed_password
        current_user.updated_at = datetime.now()

        db.commit()

        logger.info(f"Password changed for user: {current_user.username}")

        return {"message": "Password changed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

@router.post("/logout")
async def logout_user(current_user: models.User = Depends(get_current_active_user)):
    """
    Logout user
    """
    logger.info(f"User logged out: {current_user.username}")
    return {"message": "Successfully logged out"}

@router.get("/check-username/{username}")
async def check_username_availability(username: str, db: Session = Depends(get_db)):
    """
    Check if username is available
    """
    try:
        # Clean and validate username
        username = username.lower().strip()

        if len(username) < 3 or len(username) > 30:
            return {"available": False, "message": "Username must be 3-30 characters"}

        if not username.replace('_', '').replace('.', '').replace('-', '').isalnum():
            return {"available": False, "message": "Username can only contain letters, numbers, _, -, and ."}

        # Check if username exists
        existing_user = get_user_by_username(db, username)

        if existing_user:
            return {"available": False, "message": "Username is already taken"}
        else:
            return {"available": True, "message": "Username is available"}

    except Exception as e:
        logger.error(f"Username check error: {str(e)}")
        return {"available": False, "message": "Unable to check username availability"}

@router.get("/check-email/{email}")
async def check_email_availability(email: str, db: Session = Depends(get_db)):
    """
    Check if email is available
    """
    try:
        # Clean email
        email = email.lower().strip()

        # Check if email exists
        existing_user = get_user_by_email(db, email)

        if existing_user:
            return {"available": False, "message": "Email is already registered"}
        else:
            return {"available": True, "message": "Email is available"}

    except Exception as e:
        logger.error(f"Email check error: {str(e)}")
        return {"available": False, "message": "Unable to check email availability"}

@router.get("/stats")
async def get_auth_stats(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get authentication statistics
    """
    try:
        # Basic user statistics
        total_users = db.query(models.User).count()
        active_users = db.query(models.User).filter(models.User.is_active == True).count()
        restaurant_owners = db.query(models.User).filter(
            models.User.is_restaurant_owner == True,
            models.User.is_active == True
        ).count()

        # Recent registrations (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        recent_registrations = db.query(models.User).filter(
            models.User.created_at >= week_ago
        ).count()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "restaurant_owners": restaurant_owners,
            "recent_registrations": recent_registrations,
            "inactive_users": total_users - active_users
        }

    except Exception as e:
        logger.error(f"Auth stats error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch statistics"
        )

# Debug endpoint for development
@router.post("/debug/create-test-user")
async def create_test_user(db: Session = Depends(get_db)):
    """
    Create test user for development/debugging
    """
    try:
        test_user_data = UserRegister(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="test123",
            is_restaurant_owner=True
        )

        # Check if test user already exists
        existing = get_user_by_username(db, "testuser")
        if existing:
            return {"message": "Test user already exists", "username": "testuser"}

        # Create test user
        user = create_user(db, test_user_data)

        return {
            "message": "Test user created successfully",
            "username": user.username,
            "email": user.email,
            "is_restaurant_owner": user.is_restaurant_owner
        }

    except Exception as e:
        logger.error(f"Test user creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test user creation failed: {str(e)}"
        )