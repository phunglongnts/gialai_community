// ===== MAIN APPLICATION CODE =====

const { useState, useEffect, useCallback, useMemo } = React;

// ===== UTILITY FUNCTIONS =====
const utils = {
    // Debounce function for search optimization
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format price display
    formatPrice: (priceRange, averagePrice) => {
        const range = PRICE_RANGES[priceRange] || PRICE_RANGES.budget;
        let display = range.icon;

        if (averagePrice) {
            display += ` ~${averagePrice.toLocaleString('vi-VN')}đ`;
        }
        return display;
    },

    // Truncate text with ellipsis
    truncateText: (text, maxLength) => {
        if (text && text.length > maxLength) {
            return text.substring(0, maxLength) + '...';
        }
        return text || '';
    },

    // Validate Vietnamese phone number
    isValidPhone: (phone) => {
        const phoneRegex = /^(\+84|84|0)?[3|5|7|8|9][0-9]{8}$/;
        return phoneRegex.test(phone?.replace(/\s/g, ''));
    },

    // Format distance
    formatDistance: (distance) => {
        if (distance < 1) {
            return `${Math.round(distance * 1000)}m`;
        }
        return `${distance.toFixed(1)}km`;
    },

    // Get time ago string
    timeAgo: (date) => {
        const now = new Date();
        const diffMs = now - new Date(date);
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 60) return `${diffMins} phút trước`;
        if (diffHours < 24) return `${diffHours} giờ trước`;
        return `${diffDays} ngày trước`;
    }
};

// ===== API SERVICE =====
const apiService = {
    // Create axios instance
    client: axios.create({
        baseURL: CONFIG.API_BASE_URL,
        timeout: CONFIG.TIMEOUT,
        headers: {
            'Content-Type': 'application/json',
        }
    }),

    // Initialize API interceptors
    init() {
        this.client.interceptors.request.use(
            (config) => {
                console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
                return config;
            },
            (error) => Promise.reject(error)
        );

        this.client.interceptors.response.use(
            (response) => {
                console.log('✅ API Response:', response.status, response.config.url);
                return response;
            },
            (error) => {
                console.error('❌ API Error:', error.response?.status, error.message);
                return Promise.reject(error);
            }
        );
    },

    // Search restaurants with AI
    async searchRestaurants(query, options = {}) {
        try {
            const response = await this.client.post(API_ENDPOINTS.AI_SEARCH, {
                query: query.trim(),
                location: 'Gia Lai',
                preferences: {
                    include_details: true,
                    max_results: options.maxResults || CONFIG.SEARCH.MAX_RESULTS_PER_PAGE,
                    ...options
                }
            });
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    },

    // Get all restaurants
    async getRestaurants() {
        try {
            const response = await this.client.get(API_ENDPOINTS.RESTAURANTS);
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    },

    // Get restaurant details
    async getRestaurantDetails(id) {
        try {
            const endpoint = API_ENDPOINTS.RESTAURANT_DETAIL.replace('{id}', id);
            const response = await this.client.get(endpoint);
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    },

    // Check health status
    async checkHealth() {
        try {
            const response = await this.client.get(API_ENDPOINTS.HEALTH);
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    },

    // Handle API errors
    handleError(error) {
        if (error.code === 'ECONNABORTED') {
            return new Error(ERROR_MESSAGES.TIMEOUT_ERROR);
        }

        if (!error.response) {
            return new Error(ERROR_MESSAGES.NETWORK_ERROR);
        }

        const status = error.response.status;
        const message = error.response.data?.detail || error.response.data?.message;

        switch (status) {
            case 400:
                return new Error(message || ERROR_MESSAGES.INVALID_INPUT);
            case 404:
                return new Error(ERROR_MESSAGES.NOT_FOUND);
            case 401:
            case 403:
                return new Error(ERROR_MESSAGES.UNAUTHORIZED);
            case 500:
            case 502:
            case 503:
                return new Error(ERROR_MESSAGES.SERVER_ERROR);
            default:
                return new Error(message || ERROR_MESSAGES.SERVER_ERROR);
        }
    }
};

// Initialize API service
apiService.init();

// ===== REACT COMPONENTS =====

// Enhanced Header Component
const Header = () => {
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = utils.debounce(() => {
            setScrolled(window.scrollY > 50);
        }, 10);

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header className={`hero-gradient transition-all duration-500 ${scrolled ? 'shadow-2xl' : 'shadow-lg'}`}>
            <div className="container mx-auto px-6 py-6">
                <div className="header-glass rounded-2xl p-6">
                    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
                        <div className="flex items-center space-x-4 mb-4 lg:mb-0">
                            <div className="relative">
                                <i className="fas fa-utensils text-white text-4xl animate-float"></i>
                                <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
                            </div>
                            <div>
                                <h1 className="text-white text-2xl lg:text-3xl font-display font-bold mb-1">
                                    Cộng đồng Gia Lai
                                </h1>
                                <p className="text-blue-100 text-sm lg:text-base">
                                    🎯 Chơi gì? 🍜 Ăn Gì? 🏠 Ở Đâu? 👥 Với Ai?
                                </p>
                                <p className="text-blue-200 text-xs lg:text-sm mt-1">
                                    Khám phá ẩm thực, du lịch, dịch vụ với AI thông minh
                                </p>
                            </div>
                        </div>

                        <div className="flex items-center space-x-6 text-white">
                            <div className="hidden md:flex items-center space-x-2 bg-white/10 rounded-full px-4 py-2">
                                <i className="fas fa-robot text-2xl"></i>
                                <span className="font-medium">Trợ lý AI</span>
                                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                            </div>

                            <div className="flex space-x-3">
                                <button className="p-2 bg-white/10 rounded-full hover:bg-white/20 transition-colors">
                                    <i className="fas fa-heart"></i>
                                </button>
                                <button className="p-2 bg-white/10 rounded-full hover:bg-white/20 transition-colors">
                                    <i className="fas fa-share-alt"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};

// Enhanced AI Search Component
const AISearch = ({ onSearchResult }) => {
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [searchHistory, setSearchHistory] = useState([]);

    // Load search history from localStorage
    useEffect(() => {
        const history = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.SEARCH_HISTORY) || '[]');
        setSearchHistory(history);
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsLoading(true);
        setError('');
        setShowSuggestions(false);

        try {
            const result = await apiService.searchRestaurants(query.trim());
            onSearchResult(result);

            // Add to search history
            const newHistory = [query.trim(), ...searchHistory.filter(h => h !== query.trim())].slice(0, CONFIG.SEARCH.SEARCH_HISTORY_LIMIT);
            setSearchHistory(newHistory);
            localStorage.setItem(CONFIG.STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify(newHistory));

        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSuggestionClick = (suggestion) => {
        setQuery(suggestion);
        setShowSuggestions(false);
    };

    const clearSearch = () => {
        setQuery('');
        setError('');
        setShowSuggestions(false);
    };

    const suggestions = useMemo(() => {
        const combined = [...DEFAULT_SUGGESTIONS, ...searchHistory];
        return [...new Set(combined)].slice(0, CONFIG.SEARCH.SEARCH_SUGGESTIONS_COUNT);
    }, [searchHistory]);

    return (
        <div className="search-container glass-card rounded-2xl p-8 shadow-2xl mb-12 relative">
            <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mb-4 shadow-lg">
                    <i className="fas fa-search-location text-white text-2xl"></i>
                </div>
                <h2 className="text-3xl font-display font-bold text-gray-800 mb-3">
                    Tìm kiếm với AI
                </h2>
                <p className="text-gray-600 max-w-2xl mx-auto leading-relaxed">
                    Mô tả chi tiết sở thích, ngân sách và yêu cầu của bạn.
                    AI sẽ phân tích và gợi ý những địa điểm phù hợp nhất tại Gia Lai
                </p>
            </div>

            <form onSubmit={handleSearch} className="space-y-6">
                <div className="relative">
                    <div className="flex flex-col lg:flex-row gap-4">
                        <div className="flex-1 relative">
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => {
                                    setQuery(e.target.value);
                                    setError('');
                                }}
                                onFocus={() => setShowSuggestions(true)}
                                onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                                placeholder="VD: Tôi muốn ăn phở ngon, giá rẻ, gần trung tâm Pleiku, có chỗ đậu xe..."
                                className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 bg-white/80 backdrop-blur-sm"
                                disabled={isLoading}
                                maxLength={CONFIG.MAX_QUERY_LENGTH}
                            />

                            {query && !isLoading && (
                                <button
                                    type="button"
                                    onClick={clearSearch}
                                    className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                                >
                                    <i className="fas fa-times"></i>
                                </button>
                            )}

                            <div className="absolute right-2 bottom-2 text-xs text-gray-400">
                                {query.length}/{CONFIG.MAX_QUERY_LENGTH}
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading || !query.trim() || query.length < CONFIG.SEARCH.MIN_QUERY_LENGTH}
                            className="btn-primary px-8 py-4 text-white rounded-xl font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center min-w-[200px] lg:min-w-[160px]"
                        >
                            {isLoading ? (
                                <span className="flex items-center ai-thinking">
                                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
                                    AI đang phân tích...
                                </span>
                            ) : (
                                <>
                                    <i className="fas fa-search mr-3"></i>
                                    Tìm kiếm
                                </>
                            )}
                        </button>
                    </div>

                    {/* Search Suggestions */}
                    {showSuggestions && !isLoading && suggestions.length > 0 && (
                        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 max-h-80 overflow-y-auto">
                            <div className="p-4 border-b border-gray-100">
                                <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
                                    <i className="fas fa-lightbulb text-yellow-500 mr-2"></i>
                                    Gợi ý tìm kiếm
                                </h4>
                            </div>
                            {suggestions.map((suggestion, index) => (
                                <button
                                    key={index}
                                    type="button"
                                    onClick={() => handleSuggestionClick(suggestion)}
                                    className="w-full text-left px-4 py-3 hover:bg-blue-50 transition-colors border-b border-gray-50 last:border-b-0 flex items-center"
                                >
                                    <i className={`fas ${searchHistory.includes(suggestion) ? 'fa-history' : 'fa-search'} text-blue-400 mr-3`}></i>
                                    <span className="text-gray-700 flex-1">{suggestion}</span>
                                    {searchHistory.includes(suggestion) && (
                                        <span className="text-xs text-gray-400">Gần đây</span>
                                    )}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </form>

            {error && (
                <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg shadow-sm animate-fadeInScale">
                    <div className="flex items-start">
                        <i className="fas fa-exclamation-triangle text-red-500 mr-3 mt-1"></i>
                        <div className="flex-1">
                            <h4 className="font-semibold text-red-800">Không thể tìm kiếm</h4>
                            <p className="text-red-700 text-sm mt-1">{error}</p>
                            <button
                                onClick={() => setError('')}
                                className="text-red-600 underline text-sm mt-2 hover:text-red-800 transition-colors"
                            >
                                Đó