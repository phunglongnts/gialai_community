// ===== APPLICATION CONFIGURATION =====

// Main Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    TIMEOUT: 15000,
    DEBOUNCE_DELAY: 300,
    ANIMATION_DELAY: 100,
    MAX_QUERY_LENGTH: 200,

    UI: {
        LOADING_SCREEN_DURATION: 1500,
        TOAST_DURATION: 3000
    },

    SEARCH: {
        MIN_QUERY_LENGTH: 3,
        MAX_RESULTS_PER_PAGE: 12,
        SEARCH_HISTORY_LIMIT: 10
    },

    STORAGE_KEYS: {
        SEARCH_HISTORY: 'search_history',
        FAVORITES: 'favorites',
        THEME: 'theme_preference'
    },

    FEATURES: {
        ENABLE_ANALYTICS: true
    }
};

// Default search suggestions
const DEFAULT_SUGGESTIONS = [
    "Phở bò ngon, giá dưới 50k gần trung tâm",
    "Quán nhậu sân vườn có chỗ đậu xe",
    "Buffet lẩu phù hợp cho nhóm 6-8 người",
    "Cà phê view đẹp để làm việc",
    "Bánh mì chảo nổi tiếng ở Pleiku"
];

// Price ranges
const PRICE_RANGES = {
    'budget': {
        icon: '💰',
        label: 'Bình dân'
    },
    'mid-range': {
        icon: '💰💰',
        label: 'Trung bình'
    },
    'high-end': {
        icon: '💰💰💰',
        label: 'Cao cấp'
    }
};

// Restaurant categories
const RESTAURANT_CATEGORIES = {
    'vietnamese': { icon: '🍜', label: 'Món Việt' },
    'asian': { icon: '🥢', label: 'Châu Á' },
    'western': { icon: '🍕', label: 'Phương Tây' },
    'coffee': { icon: '☕', label: 'Cà phê' },
    'fastfood': { icon: '🍔', label: 'Thức ăn nhanh' }
};

// API Endpoints
const API_ENDPOINTS = {
    HEALTH: '/health',
    RESTAURANTS: '/restaurants/',
    AI_SEARCH: '/ai/search'
};

// Error messages
const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Lỗi kết nối mạng. Vui lòng kiểm tra internet.',
    SERVER_ERROR: 'Máy chủ gặp sự cố. Vui lòng thử lại sau.',
    TIMEOUT_ERROR: 'Yêu cầu quá thời gian chờ. Vui lòng thử lại.',
    SEARCH_FAILED: 'Tìm kiếm thất bại. Vui lòng thử lại.',
    NOT_FOUND: 'Không tìm thấy thông tin.'
};

// Configure Tailwind
if (typeof tailwind !== 'undefined') {
    tailwind.config = {
        theme: {
            extend: {
                fontFamily: {
                    'inter': ['Inter', 'sans-serif'],
                    'display': ['Playfair Display', 'serif'],
                },
                animation: {
                    'float': 'float 6s ease-in-out infinite',
                    'pulse-slow': 'pulse 3s ease-in-out infinite'
                }
            }
        }
    };
}

console.log('✅ Config loaded successfully');