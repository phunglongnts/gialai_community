from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


# ================================
# Base Schemas
# ================================

class UserBase(BaseModel):
    username: str = Field(..., description="Tên đăng nhập")
    email: str = Field(..., description="Email người dùng")
    full_name: str = Field(..., description="Họ và tên")
    phone: Optional[str] = Field(None, description="Số điện thoại")
    role: str = Field(default="customer", description="Vai trò: customer, restaurant_owner, admin")


class UserResponse(UserBase):
    id: int
    is_verified: bool = Field(description="Đã xác minh chưa")
    created_at: datetime

    class Config:
        from_attributes = True


# ================================
# Restaurant Creation Schemas
# ================================

class RestaurantCreateRequest(BaseModel):
    """Schema cho form tạo nhà hàng mới"""

    # Thông tin cơ bản
    name: str = Field(..., min_length=2, max_length=200, description="Tên nhà hàng")
    description: str = Field(..., min_length=10, description="Mô tả ngắn về nhà hàng")
    cuisine_type: str = Field(..., description="Loại ẩm thực: Việt Nam, Nhật Bản, Hàn Quốc, Trung Hoa, Âu, ...")

    # Địa chỉ
    address: str = Field(..., description="Địa chỉ đầy đủ")
    province: str = Field(..., description="Tỉnh/Thành phố")
    district: Optional[str] = Field(None, description="Quận/Huyện")
    ward: Optional[str] = Field(None, description="Phường/Xã")
    longitude: Optional[float] = Field(None, description="Kinh độ (từ bản đồ)")
    latitude: Optional[float] = Field(None, description="Vĩ độ (từ bản đồ)")

    # Hình ảnh (URLs sau khi upload)
    logo_url: Optional[str] = Field(None, description="URL logo nhà hàng")
    cover_image_url: Optional[str] = Field(None, description="URL ảnh bìa")
    gallery_images: Optional[List[str]] = Field(default=[], description="Danh sách URL ảnh món ăn")

    # Thông tin kinh doanh
    opening_hours: Optional[Dict[str, str]] = Field(
        default={},
        description="Giờ mở cửa: {'monday': '08:00-22:00', 'tuesday': '08:00-22:00', ...}"
    )
    price_range: Optional[str] = Field(
        default="medium",
        description="Mức giá: cheap (dưới 100k), medium (100k-300k), expensive (trên 300k)"
    )
    facilities: Optional[List[str]] = Field(
        default=[],
        description="Tiện ích: ['wifi', 'parking', 'outdoor_seating', 'air_conditioning', 'takeaway', 'delivery']"
    )

    # AI Enhancement options
    enable_ai_enhancement: bool = Field(
        default=True,
        description="Cho phép AI cải thiện mô tả và tạo nội dung"
    )

    @validator('price_range')
    def validate_price_range(cls, v):
        allowed = ['cheap', 'medium', 'expensive']
        if v not in allowed:
            raise ValueError(f'Mức giá phải là một trong: {allowed}')
        return v

    @validator('cuisine_type')
    def validate_cuisine_type(cls, v):
        # Danh sách các loại ẩm thực phổ biến tại Việt Nam
        allowed = [
            'Việt Nam', 'Nhật Bản', 'Hàn Quốc', 'Trung Hoa',
            'Thái Lan', 'Âu', 'Mỹ', 'Ấn Độ', 'Lẩu', 'BBQ',
            'Fast Food', 'Cafe', 'Bánh ngọt', 'Chay', 'Hải sản'
        ]
        if v not in allowed:
            raise ValueError(f'Loại ẩm thực không hợp lệ. Chọn từ: {allowed}')
        return v


class AIEnhancementRequest(BaseModel):
    """Schema cho request AI enhancement"""
    restaurant_data: RestaurantCreateRequest
    enhancement_options: Dict[str, bool] = Field(
        default={
            "enhance_description": True,
            "generate_menu_suggestions": True,
            "create_seo_content": True,
            "suggest_facilities": False
        },
        description="Tùy chọn AI enhancement"
    )


class AIEnhancementResponse(BaseModel):
    """Schema cho response AI enhancement"""
    enhanced_description: Optional[str] = Field(None, description="Mô tả được AI cải thiện")
    menu_suggestions: Optional[str] = Field(None, description="Gợi ý menu từ AI")
    seo_content: Optional[Dict[str, Any]] = Field(None, description="Nội dung SEO")
    suggested_facilities: Optional[List[str]] = Field(None, description="Tiện ích được gợi ý")
    processing_time: float = Field(description="Thời gian xử lý (giây)")


# ================================
# Restaurant Response Schemas
# ================================

class RestaurantResponse(BaseModel):
    """Schema cho thông tin nhà hàng đầy đủ"""
    id: int
    name: str = Field(description="Tên nhà hàng")
    description: Optional[str] = Field(description="Mô tả gốc")
    ai_enhanced_description: Optional[str] = Field(description="Mô tả được AI cải thiện")
    cuisine_type: str = Field(description="Loại ẩm thực")

    # Địa chỉ
    address: str = Field(description="Địa chỉ")
    province: str = Field(description="Tỉnh/TP")
    district: Optional[str] = Field(description="Quận/Huyện")
    ward: Optional[str] = Field(description="Phường/Xã")
    longitude: Optional[float] = Field(description="Kinh độ")
    latitude: Optional[float] = Field(description="Vĩ độ")

    # Hình ảnh
    logo_url: Optional[str] = Field(description="Logo")
    cover_image_url: Optional[str] = Field(description="Ảnh bìa")
    gallery_images: Optional[List[str]] = Field(description="Thư viện ảnh")

    # Thông tin kinh doanh
    opening_hours: Optional[Dict[str, str]] = Field(description="Giờ mở cửa")
    price_range: Optional[str] = Field(description="Mức giá")
    facilities: Optional[List[str]] = Field(description="Tiện ích")

    # AI content
    ai_menu_suggestions: Optional[str] = Field(description="Gợi ý menu AI")
    is_ai_enhanced: bool = Field(description="Đã AI enhancement")

    # Rating
    overall_rating: Optional[float] = Field(description="Điểm tổng thể")
    total_reviews: Optional[int] = Field(description="Tổng số đánh giá")

    # Trạng thái
    status: str = Field(description="Trạng thái")
    is_verified: bool = Field(description="Đã xác minh")

    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]

    # Owner info
    owner: UserResponse

    class Config:
        from_attributes = True


class RestaurantListResponse(BaseModel):
    """Schema cho danh sách nhà hàng (simplified)"""
    id: int
    name: str = Field(description="Tên nhà hàng")
    cuisine_type: str = Field(description="Loại ẩm thực")
    address: str = Field(description="Địa chỉ")
    cover_image_url: Optional[str] = Field(description="Ảnh bìa")
    price_range: Optional[str] = Field(description="Mức giá")
    overall_rating: Optional[float] = Field(description="Điểm trung bình")
    total_reviews: Optional[int] = Field(description="Số đánh giá")

    class Config:
        from_attributes = True


# ================================
# Rating & Review Schemas
# ================================

class RatingDetailResponse(BaseModel):
    """Schema cho điểm đánh giá chi tiết"""
    restaurant_id: int
    food_rating: float = Field(description="Điểm món ăn")
    service_rating: float = Field(description="Điểm phục vụ")
    atmosphere_rating: float = Field(description="Điểm không gian")
    price_rating: float = Field(description="Điểm giá cả")
    cleanliness_rating: float = Field(description="Điểm vệ sinh")
    overall_rating: float = Field(description="Điểm tổng thể")
    total_reviews: int = Field(description="Tổng số đánh giá")

    # Sentiment analysis
    positive_reviews: int = Field(description="Đánh giá tích cực")
    negative_reviews: int = Field(description="Đánh giá tiêu cực")
    neutral_reviews: int = Field(description="Đánh giá trung tính")

    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ReviewCreateRequest(BaseModel):
    """Schema cho tạo đánh giá mới"""
    restaurant_id: int = Field(description="ID nhà hàng")
    title: Optional[str] = Field(None, max_length=200, description="Tiêu đề đánh giá")
    content: str = Field(..., min_length=10, description="Nội dung đánh giá")

    # Điểm số (1-5)
    food_rating: int = Field(..., ge=1, le=5, description="Điểm món ăn (1-5)")
    service_rating: int = Field(..., ge=1, le=5, description="Điểm phục vụ (1-5)")
    atmosphere_rating: int = Field(..., ge=1, le=5, description="Điểm không gian (1-5)")
    price_rating: int = Field(..., ge=1, le=5, description="Điểm giá cả (1-5)")
    cleanliness_rating: int = Field(..., ge=1, le=5, description="Điểm vệ sinh (1-5)")


class ReviewResponse(BaseModel):
    """Schema cho đánh giá response"""
    id: int
    title: Optional[str] = Field(description="Tiêu đề")
    content: str = Field(description="Nội dung")

    # Điểm số
    food_rating: int = Field(description="Điểm món ăn")
    service_rating: int = Field(description="Điểm phục vụ")
    atmosphere_rating: int = Field(description="Điểm không gian")
    price_rating: int = Field(description="Điểm giá cả")
    cleanliness_rating: int = Field(description="Điểm vệ sinh")
    overall_rating: float = Field(description="Điểm tổng thể")

    # AI analysis
    sentiment_score: Optional[float] = Field(description="Điểm sentiment")
    sentiment_label: Optional[str] = Field(description="Nhãn sentiment")
    ai_summary: Optional[str] = Field(description="Tóm tắt AI")

    # Owner response
    owner_response: Optional[str] = Field(description="Phản hồi chủ nhà hàng")
    response_date: Optional[datetime] = Field(description="Ngày phản hồi")

    # User info
    user: UserResponse

    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class OwnerResponseRequest(BaseModel):
    """Schema cho chủ nhà hàng phản hồi review"""
    review_id: int = Field(description="ID đánh giá")
    response_content: str = Field(..., min_length=5, description="Nội dung phản hồi")


# ================================
# Dashboard Schemas
# ================================

class DashboardOverview(BaseModel):
    """Schema cho tổng quan dashboard"""
    restaurant: RestaurantResponse
    rating_summary: RatingDetailResponse

    # Thống kê tổng quan
    total_page_views: int = Field(description="Tổng lượt xem")
    total_unique_visitors: int = Field(description="Khách duy nhất")
    avg_rating: float = Field(description="Điểm trung bình")
    total_reviews: int = Field(description="Tổng đánh giá")

    # Thống kê tuần này
    weekly_views: int = Field(description="Lượt xem tuần này")
    weekly_reviews: int = Field(description="Đánh giá tuần này")

    # Top keywords tìm kiếm
    top_search_keywords: List[str] = Field(description="Từ khóa hot")

    # Recent reviews (5 cái gần nhất)
    recent_reviews: List[ReviewResponse] = Field(description="Đánh giá gần đây")


class AnalyticsData(BaseModel):
    """Schema cho dữ liệu analytics"""
    restaurant_id: int
    date_range: Dict[str, str] = Field(description="Khoảng thời gian")

    # Traffic data
    daily_views: List[Dict[str, Any]] = Field(description="Lượt xem theo ngày")
    visitor_demographics: Dict[str, int] = Field(description="Thống kê khách hàng")

    # Search data
    search_keywords: List[Dict[str, Any]] = Field(description="Từ khóa tìm kiếm")
    search_rankings: Dict[str, int] = Field(description="Thứ hạng tìm kiếm")

    # Performance metrics
    avg_session_duration: float = Field(description="Thời gian phiên trung bình")
    bounce_rate: float = Field(description="Tỷ lệ thoát")
    click_through_rate: float = Field(description="Tỷ lệ click")


# ================================
# API Response Wrappers
# ================================

class APIResponse(BaseModel):
    """Wrapper cho API response"""
    success: bool = Field(description="Thành công hay không")
    message: str = Field(description="Thông báo")
    data: Optional[Any] = Field(None, description="Dữ liệu trả về")
    error: Optional[str] = Field(None, description="Lỗi nếu có")


class PaginatedResponse(BaseModel):
    """Response có phân trang"""
    items: List[Any] = Field(description="Danh sách items")
    total: int = Field(description="Tổng số items")
    page: int = Field(description="Trang hiện tại")
    size: int = Field(description="Số items per page")
    pages: int = Field(description="Tổng số trang")


# ================================
# Menu Item Schemas
# ================================

class MenuItemCreate(BaseModel):
    """Schema tạo món ăn"""
    name: str = Field(..., description="Tên món ăn")
    description: Optional[str] = Field(None, description="Mô tả món ăn")
    price: Optional[float] = Field(None, ge=0, description="Giá món ăn")
    category: Optional[str] = Field(None, description="Danh mục: khai_vi, mon_chinh, trang_mieng, nuoc_uong")
    tags: Optional[List[str]] = Field(default=[], description="Tags: cay, chay, dac_san, pho_bien")
    image_url: Optional[str] = Field(None, description="Ảnh món ăn")
    is_available: bool = Field(default=True, description="Còn phục vụ")
    is_signature: bool = Field(default=False, description="Món đặc trưng")


class MenuItemResponse(BaseModel):
    """Schema response món ăn"""
    id: int
    name: str = Field(description="Tên món ăn")
    description: Optional[str] = Field(description="Mô tả")
    ai_enhanced_description: Optional[str] = Field(description="Mô tả AI cải thiện")
    price: Optional[float] = Field(description="Giá")
    currency: str = Field(default="VND", description="Đơn vị tiền tệ")
    category: Optional[str] = Field(description="Danh mục")
    tags: Optional[List[str]] = Field(description="Tags")
    image_url: Optional[str] = Field(description="Ảnh món ăn")
    is_available: bool = Field(description="Còn phục vụ")
    is_popular: bool = Field(description="Món phổ biến")
    is_signature: bool = Field(description="Món đặc trưng")
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ================================
# Search & Filter Schemas
# ================================

class RestaurantSearchRequest(BaseModel):
    """Schema cho tìm kiếm nhà hàng"""
    # Tìm kiếm cơ bản
    query: Optional[str] = Field(None, description="Từ khóa tìm kiếm")
    cuisine_type: Optional[str] = Field(None, description="Loại ẩm thực")
    price_range: Optional[str] = Field(None, description="Mức giá")

    # Lọc theo địa điểm
    province: Optional[str] = Field(None, description="Tỉnh/TP")
    district: Optional[str] = Field(None, description="Quận/Huyện")

    # Lọc theo rating
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Điểm tối thiểu")

    # Lọc theo tiện ích
    facilities: Optional[List[str]] = Field(default=[], description="Tiện ích cần có")

    # Sắp xếp
    sort_by: Optional[str] = Field(
        default="rating",
        description="Sắp xếp theo: rating, distance, price, newest, popular"
    )
    sort_order: Optional[str] = Field(
        default="desc",
        description="Thứ tự: asc, desc"
    )

    # Phân trang
    page: int = Field(default=1, ge=1, description="Trang")
    size: int = Field(default=10, ge=1, le=50, description="Số items per page")

    # Location-based search
    user_latitude: Optional[float] = Field(None, description="Vĩ độ người dùng")
    user_longitude: Optional[float] = Field(None, description="Kinh độ người dùng")
    max_distance: Optional[float] = Field(None, description="Khoảng cách tối đa (km)")


class AISearchRequest(BaseModel):
    """Schema cho AI search"""
    query: str = Field(..., min_length=3, description="Câu hỏi tìm kiếm bằng tiếng Việt")
    user_context: Optional[Dict[str, Any]] = Field(
        default={},
        description="Context người dùng: location, preferences, etc."
    )
    max_results: int = Field(default=5, ge=1, le=20, description="Số kết quả tối đa")


class AISearchResponse(BaseModel):
    """Schema cho AI search response"""
    query: str = Field(description="Câu hỏi gốc")
    ai_interpretation: str = Field(description="AI hiểu câu hỏi như thế nào")
    restaurants: List[RestaurantListResponse] = Field(description="Danh sách nhà hàng phù hợp")
    explanation: str = Field(description="Giải thích tại sao gợi ý những nhà hàng này")
    additional_tips: Optional[str] = Field(None, description="Lời khuyên thêm từ AI")
    processing_time: float = Field(description="Thời gian xử lý")


# ================================
# File Upload Schemas
# ================================

class ImageUploadResponse(BaseModel):
    """Schema cho response upload ảnh"""
    success: bool = Field(description="Upload thành công")
    url: str = Field(description="URL ảnh đã upload")
    filename: str = Field(description="Tên file")
    size: int = Field(description="Kích thước file (bytes)")
    content_type: str = Field(description="Loại file")


class BulkImageUploadResponse(BaseModel):
    """Schema cho upload nhiều ảnh"""
    success: bool = Field(description="Upload thành công")
    uploaded_images: List[ImageUploadResponse] = Field(description="Danh sách ảnh đã upload")
    failed_uploads: List[Dict[str, str]] = Field(description="Danh sách upload thất bại")
    total_uploaded: int = Field(description="Tổng số ảnh upload thành công")


# ================================
# Validation & Error Schemas
# ================================

class ValidationError(BaseModel):
    """Schema cho lỗi validation"""
    field: str = Field(description="Trường bị lỗi")
    message: str = Field(description="Thông báo lỗi")
    value: Any = Field(description="Giá trị bị lỗi")


class ErrorResponse(BaseModel):
    """Schema cho error response"""
    error: str = Field(description="Loại lỗi")
    message: str = Field(description="Thông báo lỗi")
    details: Optional[List[ValidationError]] = Field(None, description="Chi tiết lỗi validation")
    timestamp: datetime = Field(default_factory=datetime.now, description="Thời gian lỗi")


# ================================
# Statistics Schemas
# ================================

class RestaurantStats(BaseModel):
    """Schema thống kê nhà hàng"""
    total_restaurants: int = Field(description="Tổng số nhà hàng")
    by_cuisine: Dict[str, int] = Field(description="Thống kê theo loại ẩm thực")
    by_province: Dict[str, int] = Field(description="Thống kê theo tỉnh/TP")
    by_price_range: Dict[str, int] = Field(description="Thống kê theo mức giá")
    average_rating: float = Field(description="Điểm trung bình toàn hệ thống")

    # Top performers
    top_rated_restaurants: List[RestaurantListResponse] = Field(description="Nhà hàng đánh giá cao nhất")
    trending_restaurants: List[RestaurantListResponse] = Field(description="Nhà hàng đang hot")


class SystemHealth(BaseModel):
    """Schema cho system health check"""
    status: str = Field(description="Trạng thái hệ thống: healthy, degraded, unhealthy")
    database: str = Field(description="Trạng thái database")
    ai_service: str = Field(description="Trạng thái AI service")
    file_storage: str = Field(description="Trạng thái file storage")
    response_time: float = Field(description="Thời gian phản hồi")
    timestamp: datetime = Field(default_factory=datetime.now)


# ================================
# Chat AI Schemas
# ================================

class ChatMessage(BaseModel):
    """Schema cho tin nhắn chat"""
    message: str = Field(..., min_length=1, description="Nội dung tin nhắn")
    context: Optional[Dict[str, Any]] = Field(
        default={},
        description="Context: current_restaurant, user_location, conversation_history"
    )


class ChatResponse(BaseModel):
    """Schema cho phản hồi chat AI"""
    message: str = Field(description="Phản hồi từ AI")
    suggestions: List[str] = Field(description="Gợi ý câu hỏi tiếp theo")
    recommended_restaurants: Optional[List[RestaurantListResponse]] = Field(
        None,
        description="Nhà hàng được gợi ý (nếu có)"
    )
    session_id: str = Field(description="ID phiên chat")
    timestamp: datetime = Field(default_factory=datetime.now)