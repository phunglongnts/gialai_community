// API Configuration
window.AppConfig = {
    API_BASE_URL: 'http://localhost:8000',
    TIMEOUT: 10000,
    SITE_TITLE: 'Cộng đồng Gia Lai - Chơi gì? Ăn Gì? ở Đâu? Với Ai?',
    SITE_SUBTITLE: 'Khám phá ẩm thực, du lịch, dịch vụ với AI thông minh',
    AUTH_PAGE: 'auth_components.html',
    MESSAGES: {
        SEARCH_ERROR: 'Có lỗi xảy ra khi tìm kiếm. Vui lòng thử lại.',
        LOADING_RESTAURANTS: 'Đang tải danh sách nhà hàng...',
        NO_RESTAURANTS: 'Chưa có nhà hàng nào được thêm',
        SETUP_INSTRUCTION: 'Hãy chạy setup.py để tạo dữ liệu mẫu',
        AI_THINKING: 'AI đang suy nghĩ...',
        SEARCH_PLACEHOLDER: 'VD: Tôi muốn ăn phở ngon, giá rẻ, gần trung tâm...',
        SEARCH_DESCRIPTION: 'Mô tả sở thích của bạn, AI sẽ gợi ý nhà hàng phù hợp nhất'
    }
};

// Initialize API client
window.api = axios.create({
    baseURL: window.AppConfig.API_BASE_URL,
    timeout: window.AppConfig.TIMEOUT,
});