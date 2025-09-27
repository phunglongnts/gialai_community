from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn
from datetime import datetime
from typing import List, Optional
import json
import asyncio
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from database import get_db, engine
import models
import schemas
from services.llm_service import LLMService
from services.restaurant_service import RestaurantService

# Import authentication
from auth import get_current_user, get_current_user_optional, get_current_restaurant_owner
from routes.auth import router as auth_router

# Tạo tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Community API with Authentication",
    description="Nền tảng cộng đồng nhà hàng địa phương với AI tìm kiếm thông minh và xác thực người dùng",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Khởi tạo services
llm_service = LLMService()
restaurant_service = RestaurantService()


@app.get("/")
async def root():
    return {
        "message": "Chào mừng đến với Restaurant Community API v2.0",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "AI Search",
            "User Authentication",
            "Restaurant Management",
            "Review System"
        ],
        "auth_endpoints": "/auth/",
        "docs": "/docs"
    }


# Protected Restaurant Management Routes
@app.post("/restaurants/", response_model=schemas.RestaurantResponse)
async def create_restaurant(
        restaurant: schemas.RestaurantCreate,
        current_user: models.User = Depends(get_current_restaurant_owner),
        db: Session = Depends(get_db)
):
    """
    Tạo nhà hàng mới (Yêu cầu quyền chủ nhà hàng)
    """
    try:
        # Set owner_id to current user
        restaurant.owner_id = current_user.id
        new_restaurant = restaurant_service.create_restaurant(db, restaurant)

        logger.info(f"Restaurant created by user {current_user.username}: {new_restaurant.name}")
        return new_restaurant
    except Exception as e:
        logger.error(f"Error creating restaurant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/restaurants/", response_model=List[schemas.RestaurantResponse])
async def get_restaurants(
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """
    Lấy danh sách nhà hàng (Công khai, không cần đăng nhập)
    """
    try:
        restaurants = restaurant_service.get_restaurants(db, skip, limit, category)

        # Log for analytics if user is authenticated
        if current_user:
            logger.info(f"User {current_user.username} viewed restaurants list")

        return restaurants
    except Exception as e:
        logger.error(f"Error getting restaurants: {str(e)}")
        raise HTTPException(status_code=500, detail="Không thể lấy danh sách nhà hàng")


@app.get("/restaurants/my", response_model=List[schemas.RestaurantResponse])
async def get_my_restaurants(
        current_user: models.User = Depends(get_current_restaurant_owner),
        db: Session = Depends(get_db)
):
    """
    Lấy danh sách nhà hàng của tôi (Chỉ chủ nhà hàng)
    """
    try:
        restaurants = db.query(models.Restaurant).filter(
            models.Restaurant.owner_id == current_user.id,
            models.Restaurant.is_active == True
        ).all()

        return restaurants
    except Exception as e:
        logger.error(f"Error getting user's restaurants: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi lấy danh sách nhà hàng")


@app.get("/restaurants/{restaurant_id}", response_model=schemas.RestaurantResponse)
async def get_restaurant(
        restaurant_id: int,
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """
    Lấy thông tin chi tiết nhà hàng
    """
    try:
        restaurant = restaurant_service.get_restaurant(db, restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")

        # Log view for analytics
        if current_user:
            logger.info(f"User {current_user.username} viewed restaurant: {restaurant.name}")

        return restaurant
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting restaurant {restaurant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi server")


@app.put("/restaurants/{restaurant_id}", response_model=schemas.RestaurantResponse)
async def update_restaurant(
        restaurant_id: int,
        restaurant_update: schemas.RestaurantUpdate,
        current_user: models.User = Depends(get_current_restaurant_owner),
        db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin nhà hàng (Chỉ chủ sở hữu)
    """
    try:
        # Check ownership
        restaurant = db.query(models.Restaurant).filter(
            models.Restaurant.id == restaurant_id,
            models.Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy nhà hàng hoặc bạn không có quyền chỉnh sửa"
            )

        updated_restaurant = restaurant_service.update_restaurant(db, restaurant_id, restaurant_update)

        logger.info(f"Restaurant updated by owner {current_user.username}: {restaurant.name}")
        return updated_restaurant

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating restaurant {restaurant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi cập nhật nhà hàng")


@app.delete("/restaurants/{restaurant_id}")
async def delete_restaurant(
        restaurant_id: int,
        current_user: models.User = Depends(get_current_restaurant_owner),
        db: Session = Depends(get_db)
):
    """
    Xóa nhà hàng (Chỉ chủ sở hữu)
    """
    try:
        # Check ownership
        restaurant = db.query(models.Restaurant).filter(
            models.Restaurant.id == restaurant_id,
            models.Restaurant.owner_id == current_user.id
        ).first()

        if not restaurant:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy nhà hàng hoặc bạn không có quyền xóa"
            )

        success = restaurant_service.delete_restaurant(db, restaurant_id)

        if success:
            logger.info(f"Restaurant deleted by owner {current_user.username}: {restaurant.name}")
            return {"message": "Nhà hàng đã được xóa thành công"}
        else:
            raise HTTPException(status_code=500, detail="Không thể xóa nhà hàng")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting restaurant {restaurant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi xóa nhà hàng")


# Protected Review Routes
@app.post("/reviews/", response_model=schemas.ReviewResponse)
async def create_review(
        review: schemas.ReviewCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Tạo đánh giá mới (Yêu cầu đăng nhập)
    """
    try:
        # Set user_id to current user
        review.user_id = current_user.id

        # Check if user already reviewed this restaurant
        existing_review = db.query(models.Review).filter(
            models.Review.restaurant_id == review.restaurant_id,
            models.Review.user_id == current_user.id
        ).first()

        if existing_review:
            raise HTTPException(
                status_code=400,
                detail="Bạn đã đánh giá nhà hàng này rồi. Hãy chỉnh sửa đánh giá cũ thay vì tạo mới."
            )

        new_review = restaurant_service.create_review(db, review)

        logger.info(f"Review created by user {current_user.username} for restaurant ID {review.restaurant_id}")
        return new_review
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating review: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/reviews/my", response_model=List[schemas.ReviewResponse])
async def get_my_reviews(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Lấy danh sách đánh giá của tôi
    """
    try:
        reviews = db.query(models.Review).filter(
            models.Review.user_id == current_user.id
        ).order_by(models.Review.created_at.desc()).all()

        return reviews
    except Exception as e:
        logger.error(f"Error getting user reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi lấy danh sách đánh giá")


@app.get("/restaurants/{restaurant_id}/reviews", response_model=List[schemas.ReviewResponse])
async def get_restaurant_reviews(
        restaurant_id: int,
        skip: int = 0,
        limit: int = 10,
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """
    Lấy danh sách đánh giá của nhà hàng
    """
    try:
        reviews = restaurant_service.get_restaurant_reviews(db, restaurant_id, skip, limit)
        return reviews
    except Exception as e:
        logger.error(f"Error getting restaurant reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi lấy đánh giá")


# AI Search Routes (Enhanced with user context)
@app.post("/ai/search")
async def ai_search(
        query: schemas.AISearchRequest,
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """
    AI tìm kiếm nhà hàng thông minh với user context
    """
    start_time = time.time()

    try:
        logger.info(f"AI Search started for query: {query.query}" +
                    (f" by user {current_user.username}" if current_user else " by anonymous"))

        # Lấy tất cả nhà hàng làm context
        restaurants = restaurant_service.get_restaurants(db, 0, 50)

        if not restaurants:
            return {
                "query": query.query,
                "ai_response": "Hiện tại chưa có nhà hàng nào trong hệ thống. Hãy thêm một số nhà hàng trước!",
                "recommended_restaurants": [],
                "processing_time": time.time() - start_time,
                "user_context": "authenticated" if current_user else "anonymous",
                "timestamp": datetime.now()
            }

        # Tạo context cho LLM
        context = restaurant_service.create_search_context(restaurants)

        # Add user context if authenticated
        if current_user:
            user_context = f"\nTHÔNG TIN NGƯỜI DÙNG:\n- Tên: {current_user.full_name}\n"
            if current_user.is_restaurant_owner:
                user_context += "- Vai trò: Chủ nhà hàng\n"
            context = user_context + context

        # Gọi LLM với timeout
        result = await asyncio.wait_for(
            llm_service.search_restaurants(query.query, context),
            timeout=90.0
        )

        processing_time = time.time() - start_time
        logger.info(f"AI Search completed in {processing_time:.2f}s")

        # Log search for analytics
        if current_user:
            # Could save to AI_interactions table here
            pass

        return {
            "query": query.query,
            "ai_response": result["response"],
            "recommended_restaurants": result["recommendations"],
            "processing_time": round(processing_time, 2),
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }

    except asyncio.TimeoutError:
        processing_time = time.time() - start_time
        logger.warning(f"AI Search timeout after {processing_time:.1f}s")

        fallback_restaurants = restaurants[:3] if 'restaurants' in locals() else []

        return {
            "query": query.query,
            "ai_response": f"AI đang quá tải (timeout sau {processing_time:.1f}s). Đây là một số nhà hàng phổ biến:",
            "recommended_restaurants": fallback_restaurants,
            "processing_time": processing_time,
            "timeout": True,
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"AI search error after {processing_time}s: {str(e)}")

        fallback_restaurants = restaurants[:5] if 'restaurants' in locals() else []

        return {
            "query": query.query,
            "ai_response": f"Xin lỗi, có lỗi xảy ra với AI. Đây là danh sách nhà hàng phổ biến:",
            "recommended_restaurants": fallback_restaurants,
            "processing_time": processing_time,
            "error": str(e),
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }


@app.post("/ai/chat")
async def ai_chat(
        chat: schemas.AIChatRequest,
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """
    Chat với AI về nhà hàng với user context
    """
    start_time = time.time()

    try:
        logger.info(f"AI Chat started: {chat.message[:50]}..." +
                    (f" by user {current_user.username}" if current_user else " by anonymous"))

        # Lấy context nhà hàng
        restaurants = restaurant_service.get_restaurants(db, 0, 20)
        context = restaurant_service.create_search_context(restaurants)

        # Add user context
        if current_user:
            user_context = f"\nNGƯỜI DÙNG HIỆN TẠI:\n- Tên: {current_user.full_name}\n"
            if current_user.is_restaurant_owner:
                user_context += "- Vai trò: Chủ nhà hàng\n"
            context = user_context + context

        # Chat với LLM
        response = await asyncio.wait_for(
            llm_service.chat_with_context(chat.message, context, chat.conversation_history),
            timeout=60.0
        )

        processing_time = time.time() - start_time

        return {
            "user_message": chat.message,
            "ai_response": response,
            "processing_time": round(processing_time, 2),
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }

    except asyncio.TimeoutError:
        processing_time = time.time() - start_time
        logger.warning(f"AI Chat timeout after {processing_time:.1f}s")

        return {
            "user_message": chat.message,
            "ai_response": "Xin lỗi, AI đang quá tải. Bạn có thể thử lại sau hoặc đặt câu hỏi ngắn gọn hơn.",
            "processing_time": processing_time,
            "timeout": True,
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"AI chat error after {processing_time}s: {str(e)}")

        return {
            "user_message": chat.message,
            "ai_response": "Xin lỗi, tôi gặp sự cố kỹ thuật. Vui lòng thử lại sau.",
            "processing_time": processing_time,
            "error": str(e),
            "user_context": "authenticated" if current_user else "anonymous",
            "timestamp": datetime.now()
        }


@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái hệ thống"""
    try:
        # Kiểm tra database
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db_status = "OK"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "ERROR"

    try:
        # Kiểm tra LLM
        llm_status = await llm_service.health_check()
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")
        llm_status = "ERROR"

    # Check authentication system
    auth_status = "OK"  # Basic check - could be enhanced

    return {
        "status": "running",
        "version": "2.0.0",
        "database": db_status,
        "llm": llm_status,
        "authentication": auth_status,
        "features": {
            "user_auth": True,
            "ai_search": llm_status == "OK",
            "restaurant_crud": db_status == "OK",
            "review_system": db_status == "OK"
        },
        "timestamp": datetime.now(),
        "uptime": "running"
    }


# Analytics endpoints (Protected)
@app.get("/analytics/dashboard")
async def get_dashboard_analytics(
        current_user: models.User = Depends(get_current_restaurant_owner),
        db: Session = Depends(get_db)
):
    """
    Dashboard analytics cho chủ nhà hàng
    """
    try:
        # Get user's restaurants
        restaurants = db.query(models.Restaurant).filter(
            models.Restaurant.owner_id == current_user.id
        ).all()

        total_restaurants = len(restaurants)
        total_reviews = sum(r.total_reviews for r in restaurants)
        avg_rating = sum(
            r.average_rating * r.total_reviews for r in restaurants) / total_reviews if total_reviews > 0 else 0

        return {
            "user_id": current_user.id,
            "total_restaurants": total_restaurants,
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "restaurants": [
                {
                    "id": r.id,
                    "name": r.name,
                    "reviews": r.total_reviews,
                    "rating": r.average_rating
                } for r in restaurants
            ]
        }
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi lấy thống kê")


if __name__ == "__main__":
    print("🚀 Khởi động Restaurant Community API v2.0 với Authentication...")
    print("📱 API: http://localhost:8000")
    print("📋 Docs: http://localhost:8000/docs")
    print("🔐 Auth: http://localhost:8000/auth/")
    print("🏥 Health: http://localhost:8000/health")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )