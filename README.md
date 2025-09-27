# 🏪 Restaurant Community - Nền tảng cộng đồng nhà hàng với AI

Một nền tảng cộng đồng địa phương cho phép chủ nhà hàng tạo trang riêng, khách hàng đánh giá, và sử dụng AI để tìm kiếm nhà hàng thông minh.

## ✨ Tính năng chính

- 🤖 **AI Tìm kiếm thông minh** với Llama 3.2 3B
- 💬 **Chat AI** tư vấn nhà hàng 
- 🏪 **Quản lý nhà hàng** cho chủ cửa hàng
- 
- ⭐ **Hệ thống đánh giá** và review
- 🔍 **Tìm kiếm nâng cao** với bộ lọc
- 🛡️ **Bảo mật** với JWT authentication
- 📊 **Thống kê** và analytics

## 🛠 Công nghệ sử dụng

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **LLM**: Llama 3.2 3B (qua Ollama)
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Validation**: Pydantic

## 🚀 Cài đặt nhanh

### 1. Yêu cầu hệ thống
- Python 3.10+
- PostgreSQL 12+
- Ollama với Llama 3.2 3B
- RAM tối thiểu 8GB (cho LLM)

### 2. Clone project
```bash
git clone <repository-url>
cd restaurant_community
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình database PostgreSQL

#### Tạo database trong pgAdmin4:
1. Mở pgAdmin4
2. Tạo database mới: `restaurant_community`
3. Ghi nhớ thông tin kết nối

#### Cập nhật file `.env`:
```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin PostgreSQL của bạn
DATABASE_URL=postgresql://username:password@localhost:5432/restaurant_community
```

### 5. Cài đặt và chạy Ollama + Llama 3.2

#### Cài Ollama:
```bash
# Windows/Mac: Download từ https://ollama.ai
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Tải model Llama 3.2 3B:
```bash
ollama pull llama3.2:3b
```

#### Kiểm tra model:
```bash
ollama list
# Phải thấy llama3.2:3b trong danh sách
```

### 6. Setup database và dữ liệu mẫu
```bash
python setup.py
```

### 7. Chạy ứng dụng
```bash
python main.py
# hoặc
uvicorn main:app --reload
```

## 📱 Sử dụng API

### Truy cập API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test API cơ bản

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Lấy danh sách nhà hàng
```bash
curl http://localhost:8000/restaurants/
```

#### 3. Tìm kiếm với AI
```bash
curl -X POST "http://localhost:8000/ai/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tôi muốn tìm quán phở ngon gần đây"}'
```

#### 4. Chat với AI
```bash
curl -X POST "http://localhost:8000/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Bạn có thể gợi ý nhà hàng Nhật Bản không?"}'
```

## 🏗 Cấu trúc project

```
restaurant_community/
├── main.py              # FastAPI app chính
├── database.py          # Cấu hình database
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── setup.py             # Script setup tự động
├── requirements.txt     # Dependencies
├── .env.example         # Ví dụ cấu hình
├── services/
│   ├── llm_service.py   # Service cho LLM
│   └── restaurant_service.py # Service cho nhà hàng
└── README.md
```

## 🔧 Cấu hình nâng cao

### Tùy chỉnh LLM
Trong `.env`:
```bash
LLM_MODEL_NAME=llama3.2:3b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
OLLAMA_BASE_URL=http://localhost:11434
```

### Cấu hình CORS
```python
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Rate Limiting
```bash
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 📊 Database Schema

### Bảng chính:
- `users` - Người dùng và chủ nhà hàng
- `restaurants` - Thông tin nhà hàng
- `reviews` - Đánh giá và review
- `menu_items` - Món ăn (tương lai)
- `ai_interactions` - Lưu tương tác AI

### Mối quan hệ:
- User 1:N Restaurant (chủ nhà hàng)
- User 1:N Review  
- Restaurant 1:N Review
- Restaurant 1:N MenuItem

## 🤖 AI Features

### 1. Tìm kiếm thông minh
```python
# Ví dụ query
"Tìm quán ăn Việt Nam gần đây, giá rẻ, có chỗ đỗ xe"
"Nhà hàng nào phù hợp cho hẹn hò, view đẹp?"
"Tôi muốn ăn sushi, ngân sách khoảng 200k"
```

### 2. Chat tư vấn
- Tư vấn món ăn dựa trên sở thích
- Gợi ý nhà hàng theo dịp đặc biệt
- Phân tích review và sentiment

### 3. Phân tích review
- Tự động phân tích sentiment
- Trích xuất điểm mạnh/yếu
- Tính điểm chi tiết (món ăn, phục vụ, không gian, giá cả)

## 🛡 Bảo mật

### Authentication
- JWT tokens với refresh mechanism
- Password hashing với bcrypt
- Role-based access control

### Data Protection
- SQL injection protection (SQLAlchemy)
- Input validation (Pydantic)
- CORS configuration
- Rate limiting

### Privacy
- Đánh giá ẩn danh
- Dữ liệu local (không gửi ra ngoài)
- Encryption cho sensitive data

## 📈 Monitoring & Analytics

### Health Checks
- Database connection
- LLM availability
- System resources

### Metrics
- API response times
- Search query analysis
- User behavior tracking
- Restaurant popularity

## 🔍 Troubleshooting

### Lỗi thường gặp:

#### 1. Database connection failed
```bash
# Kiểm tra PostgreSQL
sudo systemctl status postgresql
# Kiểm tra cấu hình
psql -h localhost -U username -d restaurant_community
```

#### 2. LLM not responding
```bash
# Kiểm tra Ollama
ollama list
ollama serve
# Test model
ollama run llama3.2:3b "Hello"
```

#### 3. Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 4. Port already in use
```bash
# Tìm process đang dùng port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

## 🚀 Phát triển tiếp

### Features kế tiếp:
- [ ] Vector search với embeddings
- [ ] Real-time notifications
- [ ] Mobile app API
- [ ] Social features (follow, like)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Image upload cho nhà hàng
- [ ] Payment integration
- [ ] Booking system

### Scalability:
- [ ] Redis caching
- [ ] Database sharding
- [ ] Load balancing
- [ ] Microservices architecture
- [ ] Kubernetes deployment

## 💡 Tips phát triển

### Thêm nhà hàng mới:
```python
restaurant_data = {
    "name": "Tên nhà hàng",
    "category": "Vietnamese",
    "address": "Địa chỉ...",
    "price_range": "mid-range",
    "features": ["wifi", "parking"],
    "cuisine_types": ["Vietnamese"],
    "owner_id": 1
}
```

### Custom AI prompts:
Chỉnh sửa `system_prompt` trong `LLMService` để tùy chỉnh cách AI phản hồi.

### Thêm fields mới:
1. Cập nhật `models.py`
2. Tạo migration với Alembic
3. Cập nhật `schemas.py`
4. Cập nhật services

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong console
2. Xem file `.env` có đúng không
3. Test từng component riêng biệt
4. Kiểm tra version Python và dependencies

---

## 🎉 Chúc bạn code vui vẻ!

Đây là một dự án tuyệt vời để học Python web development kết hợp với AI. Hãy từ từ mở rộng và tùy chỉnh theo nhu cầu của bạn!