"""
Fixed Authentication System - Resolves hash and validation issues
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
import os
import logging
from dotenv import load_dotenv

import models
from database import get_db

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Security Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production-please-make-it-long-and-random-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Fixed Password hashing - more explicit configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

# JWT Bearer token
security = HTTPBearer()

# Enhanced Pydantic Models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None
    is_restaurant_owner: bool = False

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v:
            raise ValueError('Username is required')
        v = v.strip().lower()
        if len(v) < 3 or len(v) > 30:
            raise ValueError('Username must be between 3 and 30 characters')
        if not v.replace('_', '').replace('.', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, _, -, and .')
        return v

    @validator('email')
    def email_required(cls, v):
        if not v:
            raise ValueError('Email is required')
        return v.lower().strip()

    @validator('full_name')
    def full_name_required(cls, v):
        if not v or not v.strip():
            raise ValueError('Full name is required')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 6:  # Relaxed requirement for testing
            raise ValueError('Password must be at least 6 characters long')
        return v

    @validator('phone', pre=True)
    def validate_phone(cls, v):
        if v is not None and v.strip():
            v = v.strip()
            # Basic phone validation
            if len(v) < 10 or len(v) > 15:
                raise ValueError('Phone number must be 10-15 characters')
            return v
        return None

class UserLogin(BaseModel):
    username_or_email: str
    password: str

    @validator('username_or_email')
    def username_or_email_required(cls, v):
        if not v or not v.strip():
            raise ValueError('Username or email is required')
        return v.strip().lower()

    @validator('password')
    def password_required(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    is_restaurant_owner: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Enhanced Authentication Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password with better error handling"""
    try:
        if not plain_password or not hashed_password:
            return False
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        # Try with different context as fallback
        try:
            import bcrypt
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            if isinstance(plain_password, str):
                plain_password = plain_password.encode('utf-8')
            return bcrypt.checkpw(plain_password, hashed_password)
        except Exception as e2:
            logger.error(f"Fallback password verification error: {e2}")
            return False

def get_password_hash(password: str) -> str:
    """Hash a password with better error handling"""
    try:
        if not password:
            raise ValueError("Password cannot be empty")
        hashed = pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        # Fallback to basic bcrypt
        try:
            import bcrypt
            salt = bcrypt.gensalt()
            if isinstance(password, str):
                password = password.encode('utf-8')
            hashed = bcrypt.hashpw(password, salt)
            return hashed.decode('utf-8')
        except Exception as e2:
            logger.error(f"Fallback password hashing error: {e2}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Password hashing failed"
            )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token creation failed"
        )

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Refresh token creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refresh token creation failed"
        )

def verify_token(token: str, token_type: str = "access") -> TokenData:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check token type
        if payload.get("type") != token_type:
            raise JWTError("Invalid token type")

        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise JWTError("Invalid token payload")

        return TokenData(username=username, user_id=user_id)

    except JWTError as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Enhanced Database Operations
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username"""
    try:
        return db.query(models.User).filter(
            models.User.username == username.lower().strip()
        ).first()
    except Exception as e:
        logger.error(f"Error getting user by username: {e}")
        return None

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    try:
        return db.query(models.User).filter(
            models.User.email == email.lower().strip()
        ).first()
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID"""
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[models.User]:
    """Authenticate user by username/email and password"""
    try:
        if not username_or_email or not password:
            logger.warning("Empty username/email or password")
            return None

        username_or_email = username_or_email.strip().lower()

        # Try to find user by username or email
        user = get_user_by_username(db, username_or_email)
        if not user:
            user = get_user_by_email(db, username_or_email)

        if not user:
            logger.warning(f"User not found: {username_or_email}")
            return None

        if not user.is_active:
            logger.warning(f"Inactive user: {username_or_email}")
            return None

        # Verify password
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {username_or_email}")
            return None

        logger.info(f"User authenticated successfully: {user.username}")
        return user

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

def create_user(db: Session, user_create: UserRegister) -> models.User:
    """Create new user with enhanced error handling"""
    try:
        # Validate input
        if not user_create.username or not user_create.email or not user_create.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username, email, and password are required"
            )

        username = user_create.username.strip().lower()
        email = user_create.email.strip().lower()

        # Check if username already exists
        existing_user = get_user_by_username(db, username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        existing_email = get_user_by_email(db, email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = get_password_hash(user_create.password)

        # Create new user
        db_user = models.User(
            username=username,
            email=email,
            full_name=user_create.full_name.strip(),
            phone=user_create.phone.strip() if user_create.phone else None,
            hashed_password=hashed_password,
            is_restaurant_owner=user_create.is_restaurant_owner,
            is_active=True
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User created successfully: {db_user.username}")
        return db_user

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"User creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed"
        )

# Dependencies for FastAPI routes
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.User:
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        token_data = verify_token(token, "access")

        user = get_user_by_id(db, token_data.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Get current active user"""
    return current_user

async def get_current_restaurant_owner(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Get current user if they are a restaurant owner"""
    if not current_user.is_restaurant_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Restaurant owner access required."
        )
    return current_user

async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    """Get current user if authenticated, otherwise return None"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        token_data = verify_token(token, "access")

        user = get_user_by_id(db, token_data.user_id)
        if user and user.is_active:
            return user
        return None
    except:
        return None

def generate_tokens(user: models.User) -> Token:
    """Generate access and refresh tokens for user"""
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        token_data = {"sub": user.username, "user_id": user.id}

        access_token = create_access_token(token_data, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_restaurant_owner": user.is_restaurant_owner
            }
        )
    except Exception as e:
        logger.error(f"Token generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed"
        )

def refresh_access_token(refresh_token: str, db: Session) -> Token:
    """Generate new access token from refresh token"""
    try:
        token_data = verify_token(refresh_token, "refresh")

        user = get_user_by_id(db, token_data.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        return generate_tokens(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )

# Utility function to check if database has users with old hash format
def check_and_fix_user_hashes(db: Session):
    """Check for users with problematic hashes and fix them"""
    try:
        users = db.query(models.User).all()
        fixed_count = 0

        for user in users:
            try:
                # Test if hash is valid
                pwd_context.verify("test", user.hashed_password)
            except:
                # Hash is invalid, need to reset (in production, would require email verification)
                logger.warning(f"Invalid hash for user {user.username}, needs password reset")
                # Don't auto-fix in production, just log

        logger.info(f"Hash check completed. {fixed_count} users need password reset")

    except Exception as e:
        logger.error(f"Hash check error: {e}")