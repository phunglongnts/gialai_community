# Restaurant Community Frontend

Frontend cho ứng dụng cộng đồng ẩm thực với tính năng AI.

## Cấu trúc thư mục
frontend/
├── index.html              # Trang chính
├── auth_components.html    # Trang đăng nhập/đăng ký
├── config/
│   └── config.js          # Cấu hình API và messages
├── themes/
│   ├── default.css        # Theme mặc định
│   └── dark.css          # Theme tối (ví dụ)
├── components/
│   ├── Header.js          # Component header
│   ├── AISearch.js        # Component tìm kiếm AI
│   ├── RestaurantCard.js  # Component card nhà hàng
│   ├── AIResponse.js      # Component hiển thị phản hồi AI
│   ├── RestaurantList.js  # Component danh sách nhà hàng
│   └── StatusIndicator.js # Component hiển thị trạng thái API
├── js/
│   └── app.js            # Main application logic
└── assets/               # Tài nguyên (hình ảnh, font, etc.)

Nếu bạn muốn cho phép chạy script vĩnh viễn (không cần cài lại mỗi lần mở PowerShell), chạy:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

chạy trên powershell
npx serve . -l 3000