from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, DECIMAL, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime

Base = declarative_base()


class User(Base):
    """Model người dùng hệ thống"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(String(20), default="customer")  # customer, restaurant_owner, admin
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    restaurant = relationship("Restaurant", back_populates="owner", uselist=False)
    reviews = relationship("Review", back_populates="user")
    ai_interactions = relationship("AIInteraction", back_populates="user")


class Restaurant(Base):
    """Model nhà hàng với AI enhancement"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Thông tin cơ bản
    name = Column(String(200), nullable=False, index=True, comment="Tên nhà hàng")
    description = Column(Text, comment="Mô tả do chủ nhà hàng nhập")
    ai_enhanced_description = Column(Text, comment="Mô tả được AI cải thiện")
    cuisine_type = Column(String(100), nullable=False, comment="Loại ẩm thực")

    # Địa chỉ và vị trí
    address = Column(String(500), nullable=False, comment="Địa chỉ đầy đủ")
    province = Column(String(100), nullable=False, comment="Tỉnh/Thành phố")
    district = Column(String(100), comment="Quận/Huyện")
    ward = Column(String(100), comment="Phường/Xã")
    longitude = Column(DECIMAL(10, 8), comment="Kinh độ")
    latitude = Column(DECIMAL(10, 8), comment="Vĩ độ")

    # Hình ảnh
    logo_url = Column(String(500), comment="Đường dẫn logo nhà hàng")
    cover_image_url = Column(String(500), comment="Ảnh bìa nhà hàng")
    gallery_images = Column(ARRAY(String), comment="Thư viện ảnh món ăn")

    # Thông tin kinh doanh
    opening_hours = Column(JSON, comment="Giờ mở cửa theo ngày trong tuần")
    price_range = Column(String(20), comment="Mức giá: cheap, medium, expensive")
    facilities = Column(ARRAY(String), comment="Tiện ích: wifi, parking, outdoor_seating, etc.")

    # AI Generated Content
    ai_menu_suggestions = Column(Text, comment="Gợi ý menu do AI tạo")
    ai_seo_content = Column(JSON, comment="Nội dung SEO do AI tạo")
    is_ai_enhanced = Column(Boolean, default=False, comment="Đã được AI cải thiện")

    # Trạng thái
    status = Column(String(20), default="active", comment="Trạng thái: active, inactive, pending")
    is_verified = Column(Boolean, default=False, comment="Đã được xác minh")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
    rating_details = relationship("RatingDetail", back_populates="restaurant", uselist=False)
    menu_items = relationship("MenuItem", back_populates="restaurant")


class RatingDetail(Base):
    """Bảng điểm đánh giá chi tiết theo từng khía cạnh"""
    __tablename__ = "rating_details"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), unique=True, nullable=False)

    # Điểm chi tiết (1-5 sao)
    food_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm chất lượng món ăn")
    service_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm phục vụ")
    atmosphere_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm không gian")
    price_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm giá cả hợp lý")
    cleanliness_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm vệ sinh")

    # Điểm tổng và thống kê
    overall_rating = Column(DECIMAL(2, 1), default=0, comment="Điểm tổng thể")
    total_reviews = Column(Integer, default=0, comment="Tổng số đánh giá")

    # Phân tích sentiment
    positive_reviews = Column(Integer, default=0, comment="Số review tích cực")
    negative_reviews = Column(Integer, default=0, comment="Số review tiêu cực")
    neutral_reviews = Column(Integer, default=0, comment="Số review trung tính")

    # Timestamps
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    restaurant = relationship("Restaurant", back_populates="rating_details")


class Review(Base):
    """Bảng đánh giá nhà hàng"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    # Nội dung đánh giá
    title = Column(String(200), comment="Tiêu đề đánh giá")
    content = Column(Text, nullable=False, comment="Nội dung đánh giá")

    # Điểm số chi tiết
    food_rating = Column(Integer, nullable=False, comment="Điểm món ăn (1-5)")
    service_rating = Column(Integer, nullable=False, comment="Điểm phục vụ (1-5)")
    atmosphere_rating = Column(Integer, nullable=False, comment="Điểm không gian (1-5)")
    price_rating = Column(Integer, nullable=False, comment="Điểm giá cả (1-5)")
    cleanliness_rating = Column(Integer, nullable=False, comment="Điểm vệ sinh (1-5)")
    overall_rating = Column(DECIMAL(2, 1), nullable=False, comment="Điểm tổng thể")

    # AI Analysis
    sentiment_score = Column(DECIMAL(3, 2), comment="Điểm sentiment (-1 đến 1)")
    sentiment_label = Column(String(20), comment="Nhãn sentiment: positive, negative, neutral")
    ai_summary = Column(Text, comment="Tóm tắt đánh giá do AI tạo")

    # Phản hồi từ chủ nhà hàng
    owner_response = Column(Text, comment="Phản hồi từ chủ nhà hàng")
    response_date = Column(DateTime(timezone=True), comment="Ngày phản hồi")

    # Trạng thái
    is_verified = Column(Boolean, default=False, comment="Đã xác minh")
    is_featured = Column(Boolean, default=False, comment="Đánh giá nổi bật")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")


class MenuItem(Base):
    """Bảng món ăn trong menu"""
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    # Thông tin món ăn
    name = Column(String(200), nullable=False, comment="Tên món ăn")
    description = Column(Text, comment="Mô tả món ăn")
    ai_enhanced_description = Column(Text, comment="Mô tả được AI cải thiện")

    # Giá cả
    price = Column(DECIMAL(10, 2), comment="Giá món ăn")
    currency = Column(String(10), default="VND", comment="Đơn vị tiền tệ")

    # Phân loại
    category = Column(String(100), comment="Danh mục món ăn")
    tags = Column(ARRAY(String), comment="Thẻ tag: spicy, vegetarian, signature, etc.")

    # Hình ảnh
    image_url = Column(String(500), comment="Ảnh món ăn")

    # Trạng thái
    is_available = Column(Boolean, default=True, comment="Còn phục vụ")
    is_popular = Column(Boolean, default=False, comment="Món phổ biến")
    is_signature = Column(Boolean, default=False, comment="Món đặc trưng")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    restaurant = relationship("Restaurant", back_populates="menu_items")


class AIInteraction(Base):
    """Bảng lưu tương tác với AI"""
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Nội dung tương tác
    interaction_type = Column(String(50), nullable=False, comment="Loại tương tác: search, chat, enhancement")
    user_input = Column(Text, nullable=False, comment="Input từ người dùng")
    ai_response = Column(Text, nullable=False, comment="Phản hồi từ AI")

    # Metadata
    session_id = Column(String(100), comment="ID phiên làm việc")
    processing_time = Column(DECIMAL(5, 3), comment="Thời gian xử lý (giây)")
    model_used = Column(String(50), comment="Model AI được sử dụng")

    # Context
    restaurant_context = Column(Integer, ForeignKey("restaurants.id"), comment="Nhà hàng liên quan")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="ai_interactions")


class RestaurantAnalytics(Base):
    """Bảng thống kê analytics cho nhà hàng"""
    __tablename__ = "restaurant_analytics"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    # Thống kê theo ngày
    date = Column(DateTime(timezone=True), nullable=False, comment="Ngày thống kê")
    page_views = Column(Integer, default=0, comment="Lượt xem trang")
    unique_visitors = Column(Integer, default=0, comment="Khách truy cập duy nhất")
    search_impressions = Column(Integer, default=0, comment="Số lần xuất hiện trong tìm kiếm")
    click_through_rate = Column(DECIMAL(5, 2), comment="Tỷ lệ click (CTR)")

    # Engagement metrics
    avg_time_on_page = Column(DECIMAL(8, 2), comment="Thời gian trung bình trên trang (giây)")
    bounce_rate = Column(DECIMAL(5, 2), comment="Tỷ lệ thoát")

    # Search keywords
    top_keywords = Column(JSON, comment="Từ khóa tìm kiếm hàng đầu")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())