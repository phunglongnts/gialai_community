import React, { useState, useEffect } from 'react';
import {
  BarChart3, Star, Users, Eye, TrendingUp, MessageSquare,
  Settings, Edit3, Calendar, MapPin, Phone, Mail, Clock,
  ChevronDown, ChevronUp, Filter, Download, RefreshCw
} from 'lucide-react';

const RestaurantDashboard = () => {
  // State management
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7days');

  // Mock data - thay thế bằng API calls thực tế
  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      setDashboardData({
        restaurant: {
          id: 1,
          name: "Nhà hàng Hương Việt",
          cuisine_type: "Việt Nam",
          address: "123 Trần Hưng Đạo, Pleiku, Gia Lai",
          logo_url: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=100&h=100&fit=crop&crop=center",
          cover_image_url: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=300&fit=crop",
          phone: "0269.123.456",
          email: "contact@huongviet.com",
          status: "active",
          is_verified: true
        },
        stats: {
          overall_rating: 4.3,
          total_reviews: 127,
          weekly_views: 1247,
          weekly_visitors: 892,
          total_page_views: 5678,
          total_unique_visitors: 3421
        },
        rating_breakdown: {
          food_rating: 4.5,
          service_rating: 4.2,
          atmosphere_rating: 4.1,
          price_rating: 4.4,
          cleanliness_rating: 4.3,
          positive_reviews: 89,
          negative_reviews: 12,
          neutral_reviews: 26
        },
        recent_reviews: [
          {
            id: 1,
            user: { full_name: "Nguyễn Văn An", avatar: null },
            overall_rating: 5,
            title: "Món ăn rất ngon!",
            content: "Phở ở đây rất đậm đà, thịt bò tươi ngon. Nhân viên phục vụ nhiệt tình.",
            created_at: "2024-01-15T10:30:00Z",
            sentiment_label: "positive"
          },
          {
            id: 2,
            user: { full_name: "Trần Thị Bình", avatar: null },
            overall_rating: 4,
            title: "Không gian đẹp",
            content: "Nhà hàng trang trí đẹp, tuy nhiên thời gian chờ món hơi lâu.",
            created_at: "2024-01-14T19:45:00Z",
            sentiment_label: "neutral"
          },
          {
            id: 3,
            user: { full_name: "Lê Minh Châu", avatar: null },
            overall_rating: 3,
            title: "Cần cải thiện",
            content: "Món ăn ổn nhưng phục vụ chưa được chuyên nghiệp lắm.",
            created_at: "2024-01-13T14:20:00Z",
            sentiment_label: "negative"
          }
        ],
        top_keywords: ["phở ngon", "nhà hàng việt", "pleiku ăn gì", "món ngon gia lai"],
        analytics: {
          daily_views: [
            { date: "2024-01-10", views: 45, visitors: 32 },
            { date: "2024-01-11", views: 67, visitors: 41 },
            { date: "2024-01-12", views: 89, visitors: 56 },
            { date: "2024-01-13", views: 123, visitors: 78 },
            { date: "2024-01-14", views: 156, visitors: 95 },
            { date: "2024-01-15", views: 178, visitors: 112 },
            { date: "2024-01-16", views: 203, visitors: 134 }
          ]
        }
      });
      setLoading(false);
    };

    fetchDashboardData();
  }, [timeRange]);

  // Helper functions
  const formatNumber = (num) => {
    return new Intl.NumberFormat('vi-VN').format(num);
  };

  const formatDate = (dateString) => {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(dateString));
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getRatingStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${
          i < Math.floor(rating)
            ? 'text-yellow-400 fill-current'
            : 'text-gray-300'
        }`}
      />
    ));
  };

  // Tab components
  const tabs = [
    { key: 'overview', label: 'Tổng quan', icon: BarChart3 },
    { key: 'reviews', label: 'Đánh giá', icon: MessageSquare },
    { key: 'analytics', label: 'Thống kê', icon: TrendingUp },
    { key: 'settings', label: 'Cài đặt', icon: Settings }
  ];

  // Overview Tab Component
  const OverviewTab = () => (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Star className="w-6 h-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Điểm trung bình</p>
              <p className="text-2xl font-bold text-gray-900">
                {dashboardData.stats.overall_rating}
                <span className="text-sm text-gray-500 ml-1">/ 5.0</span>
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <MessageSquare className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Tổng đánh giá</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(dashboardData.stats.total_reviews)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Eye className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Lượt xem tuần</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(dashboardData.stats.weekly_views)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Khách mới tuần</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(dashboardData.stats.weekly_visitors)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Restaurant Info Card */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="relative">
          <img
            src={dashboardData.restaurant.cover_image_url}
            alt="Cover"
            className="w-full h-48 object-cover"
          />
          <div className="absolute top-4 right-4">
            <button className="bg-white bg-opacity-90 hover:bg-opacity-100 px-3 py-1 rounded-full text-sm font-medium text-gray-700 transition-all">
              <Edit3 className="w-4 h-4 inline mr-1" />
              Chỉnh sửa
            </button>
          </div>
        </div>

        <div className="p-6">
          <div className="flex items-start space-x-4">
            <img
              src={dashboardData.restaurant.logo_url}
              alt="Logo"
              className="w-16 h-16 rounded-lg object-cover border-2 border-white shadow-sm"
            />
            <div className="flex-1">
              <div className="flex items-center space-x-2">
                <h2 className="text-xl font-bold text-gray-900">{dashboardData.restaurant.name}</h2>
                {dashboardData.restaurant.is_verified && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    ✓ Đã xác minh
                  </span>
                )}
              </div>
              <p className="text-gray-600 mt-1">{dashboardData.restaurant.cuisine_type}</p>
              <div className="flex items-center text-gray-500 mt-2 space-x-4">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  <span className="text-sm">{dashboardData.restaurant.address}</span>
                </div>
              </div>
              <div className="flex items-center text-gray-500 mt-2 space-x-4">
                <div className="flex items-center">
                  <Phone className="w-4 h-4 mr-1" />
                  <span className="text-sm">{dashboardData.restaurant.phone}</span>
                </div>
                <div className="flex items-center">
                  <Mail className="w-4 h-4 mr-1" />
                  <span className="text-sm">{dashboardData.restaurant.email}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Rating Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Điểm đánh giá chi tiết</h3>
          <div className="space-y-4">
            {[
              { label: 'Chất lượng món ăn', rating: dashboardData.rating_breakdown.food_rating, color: 'bg-green-500' },
              { label: 'Phục vụ', rating: dashboardData.rating_breakdown.service_rating, color: 'bg-blue-500' },
              { label: 'Không gian', rating: dashboardData.rating_breakdown.atmosphere_rating, color: 'bg-purple-500' },
              { label: 'Giá cả hợp lý', rating: dashboardData.rating_breakdown.price_rating, color: 'bg-yellow-500' },
              { label: 'Vệ sinh', rating: dashboardData.rating_breakdown.cleanliness_rating, color: 'bg-indigo-500' }
            ].map((item, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="w-24 text-sm text-gray-600">{item.label}</div>
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${item.color}`}
                    style={{ width: `${(item.rating / 5) * 100}%` }}
                  />
                </div>
                <div className="w-12 text-right text-sm font-medium text-gray-900">
                  {item.rating}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Phân tích cảm xúc</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Tích cực</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.rating_breakdown.positive_reviews} đánh giá
                </span>
                <span className="text-sm text-gray-500">
                  ({Math.round((dashboardData.rating_breakdown.positive_reviews / dashboardData.stats.total_reviews) * 100)}%)
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Trung tính</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.rating_breakdown.neutral_reviews} đánh giá
                </span>
                <span className="text-sm text-gray-500">
                  ({Math.round((dashboardData.rating_breakdown.neutral_reviews / dashboardData.stats.total_reviews) * 100)}%)
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Tiêu cực</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.rating_breakdown.negative_reviews} đánh giá
                </span>
                <span className="text-sm text-gray-500">
                  ({Math.round((dashboardData.rating_breakdown.negative_reviews / dashboardData.stats.total_reviews) * 100)}%)
                </span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Hành động nhanh</h4>
            <div className="space-y-2">
              <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                📊 Xem báo cáo chi tiết
              </button>
              <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                💬 Phản hồi đánh giá chưa trả lời
              </button>
              <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                🚀 Tối ưu trang nhà hàng
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Reviews */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">Đánh giá gần đây</h3>
          <button
            onClick={() => setActiveTab('reviews')}
            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            Xem tất cả →
          </button>
        </div>

        <div className="space-y-4">
          {dashboardData.recent_reviews.slice(0, 3).map((review) => (
            <div key={review.id} className="border-b border-gray-200 pb-4 last:border-b-0 last:pb-0">
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-gray-700">
                    {review.user.full_name.charAt(0)}
                  </span>
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h4 className="font-medium text-gray-900">{review.user.full_name}</h4>
                    <div className="flex items-center">
                      {getRatingStars(review.overall_rating)}
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(review.sentiment_label)}`}>
                      {review.sentiment_label === 'positive' ? 'Tích cực' :
                       review.sentiment_label === 'negative' ? 'Tiêu cực' : 'Trung tính'}
                    </span>
                  </div>
                  {review.title && (
                    <h5 className="text-sm font-medium text-gray-900 mt-1">{review.title}</h5>
                  )}
                  <p className="text-sm text-gray-600 mt-1">{review.content}</p>
                  <p className="text-xs text-gray-500 mt-2">{formatDate(review.created_at)}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Search Keywords */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Từ khóa tìm kiếm hàng đầu</h3>
        <div className="flex flex-wrap gap-2">
          {dashboardData.top_keywords.map((keyword, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
            >
              {keyword}
            </span>
          ))}
        </div>
      </div>
    </div>
  );

  // Reviews Tab Component
  const ReviewsTab = () => {
    const [reviewFilter, setReviewFilter] = useState('all');
    const [sortBy, setSortBy] = useState('newest');

    return (
      <div className="space-y-6">
        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex flex-wrap items-center gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lọc theo</label>
              <select
                value={reviewFilter}
                onChange={(e) => setReviewFilter(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="all">Tất cả đánh giá</option>
                <option value="positive">Tích cực</option>
                <option value="neutral">Trung tính</option>
                <option value="negative">Tiêu cực</option>
                <option value="5star">5 sao</option>
                <option value="4star">4 sao</option>
                <option value="3star">3 sao</option>
                <option value="2star">2 sao</option>
                <option value="1star">1 sao</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sắp xếp</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="newest">Mới nhất</option>
                <option value="oldest">Cũ nhất</option>
                <option value="highest">Điểm cao nhất</option>
                <option value="lowest">Điểm thấp nhất</option>
              </select>
            </div>

            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors">
              <Filter className="w-4 h-4 inline mr-2" />
              Áp dụng
            </button>

            <button className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors ml-auto">
              <Download className="w-4 h-4 inline mr-2" />
              Xuất Excel
            </button>
          </div>
        </div>

        {/* Reviews List */}
        <div className="space-y-4">
          {dashboardData.recent_reviews.map((review) => (
            <div key={review.id} className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center">
                  <span className="font-medium text-gray-700">
                    {review.user.full_name.charAt(0)}
                  </span>
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <h4 className="font-medium text-gray-900">{review.user.full_name}</h4>
                      <div className="flex items-center">
                        {getRatingStars(review.overall_rating)}
                        <span className="ml-2 text-sm text-gray-600">({review.overall_rating}/5)</span>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(review.sentiment_label)}`}>
                        {review.sentiment_label === 'positive' ? 'Tích cực' :
                         review.sentiment_label === 'negative' ? 'Tiêu cực' : 'Trung tính'}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500">
                      {formatDate(review.created_at)}
                    </div>
                  </div>

                  {review.title && (
                    <h5 className="font-medium text-gray-900 mt-2">{review.title}</h5>
                  )}

                  <p className="text-gray-700 mt-2 leading-relaxed">{review.content}</p>

                  {/* Rating breakdown */}
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-gray-600">Món ăn</div>
                        <div className="font-medium">4.5/5</div>
                      </div>
                      <div className="text-center">
                        <div className="text-gray-600">Phục vụ</div>
                        <div className="font-medium">4.0/5</div>
                      </div>
                      <div className="text-center">
                        <div className="text-gray-600">Không gian</div>
                        <div className="font-medium">4.2/5</div>
                      </div>
                      <div className="text-center">
                        <div className="text-gray-600">Giá cả</div>
                        <div className="font-medium">4.3/5</div>
                      </div>
                      <div className="text-center">
                        <div className="text-gray-600">Vệ sinh</div>
                        <div className="font-medium">4.4/5</div>
                      </div>
                    </div>
                  </div>

                  {/* Action buttons */}
                  <div className="mt-4 flex items-center space-x-3">
                    <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">
                      💬 Phản hồi
                    </button>
                    <button className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg hover:bg-gray-200 transition-colors">
                      ⭐ Đánh dấu nổi bật
                    </button>
                    <button className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg hover:bg-gray-200 transition-colors">
                      🚨 Báo cáo
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Load more */}
        <div className="text-center">
          <button className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            Tải thêm đánh giá
          </button>
        </div>
      </div>
    );
  };

  // Analytics Tab Component
  const AnalyticsTab = () => (
    <div className="space-y-6">
      {/* Time Range Selector */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Thống kê chi tiết</h3>
          <div className="flex items-center space-x-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
            >
              <option value="7days">7 ngày qua</option>
              <option value="30days">30 ngày qua</option>
              <option value="90days">3 tháng qua</option>
              <option value="1year">1 năm qua</option>
            </select>
            <button className="p-2 text-gray-400 hover:text-gray-600">
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Page Views Chart */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Lượt xem theo ngày</h4>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <div className="text-center">
              <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-600">Biểu đồ lượt xem sẽ hiển thị ở đây</p>
            </div>
          </div>
        </div>

        {/* Visitor Sources */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Nguồn khách hàng</h4>
          <div className="space-y-3">
            {[
              { source: 'Tìm kiếm Google', percentage: 45, count: '1,247 lượt' },
              { source: 'Trực tiếp', percentage: 30, count: '832 lượt' },
              { source: 'Facebook', percentage: 15, count: '416 lượt' },
              { source: 'Instagram', percentage: 10, count: '277 lượt' }
            ].map((item, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="flex-1">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-700">{item.source}</span>
                    <span className="text-gray-500">{item.count}</span>
                  </div>
                  <div className="bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${item.percentage}%` }}
                    />
                  </div>
                </div>
                <div className="text-sm font-medium text-gray-900 w-12 text-right">
                  {item.percentage}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Hiệu suất trang</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Thời gian trung bình</span>
              <span className="font-medium">2m 34s</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tỷ lệ thoát</span>
              <span className="font-medium">32%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tỷ lệ click</span>
              <span className="font-medium">4.7%</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Thiết bị truy cập</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Mobile</span>
              <span className="font-medium">68%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Desktop</span>
              <span className="font-medium">28%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tablet</span>
              <span className="font-medium">4%</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Thời gian cao điểm</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">11:00 - 13:00</span>
              <span className="font-medium">🔥 Peak</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">18:00 - 20:00</span>
              <span className="font-medium">📈 Cao</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">21:00 - 23:00</span>
              <span className="font-medium">📊 Trung bình</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Settings Tab Component
  const SettingsTab = () => (
    <div className="space-y-6">
      {/* Restaurant Basic Info */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Thông tin cơ bản</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Tên nhà hàng</label>
            <input
              type="text"
              defaultValue={dashboardData.restaurant.name}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Loại ẩm thực</label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="Việt Nam" selected>Việt Nam</option>
              <option value="Nhật Bản">Nhật Bản</option>
              <option value="Hàn Quốc">Hàn Quốc</option>
              <option value="Trung Hoa">Trung Hoa</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Số điện thoại</label>
            <input
              type="tel"
              defaultValue={dashboardData.restaurant.phone}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              defaultValue={dashboardData.restaurant.email}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Địa chỉ</label>
          <textarea
            defaultValue={dashboardData.restaurant.address}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="mt-6">
          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            💾 Lưu thay đổi
          </button>
        </div>
      </div>

      {/* Opening Hours */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Giờ mở cửa</h3>
        <div className="space-y-3">
          {[
            'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm',
            'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật'
          ].map((day, index) => (
            <div key={index} className="flex items-center space-x-4">
              <div className="w-20 text-sm font-medium text-gray-700">{day}</div>
              <input
                type="text"
                defaultValue="08:00-22:00"
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="VD: 08:00-22:00 hoặc Đóng cửa"
              />
            </div>
          ))}
        </div>
        <div className="mt-6">
          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            💾 Cập nhật giờ mở cửa
          </button>
        </div>
      </div>

      {/* AI & Automation */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-medium text-gray-900 mb-4">AI & Tự động hóa</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-gray-900">Tự động phản hồi đánh giá</h4>
              <p className="text-sm text-gray-600">AI sẽ tự động tạo phản hồi cho đánh giá mới</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-gray-900">Gợi ý cải thiện thông tin</h4>
              <p className="text-sm text-gray-600">Nhận gợi ý từ AI để tối ưu trang nhà hàng</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" defaultChecked className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-gray-900">Báo cáo analytics hàng tuần</h4>
              <p className="text-sm text-gray-600">Nhận email báo cáo hiệu suất mỗi tuần</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" defaultChecked className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="bg-red-50 border border-red-200 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-red-900 mb-4">⚠️ Vùng nguy hiểm</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-red-900">Tạm dừng nhà hàng</h4>
              <p className="text-sm text-red-700">Nhà hàng sẽ không hiển thị với khách hàng</p>
            </div>
            <button className="px-4 py-2 bg-yellow-600 text-white text-sm rounded-lg hover:bg-yellow-700 transition-colors">
              Tạm dừng
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-red-900">Xóa nhà hàng</h4>
              <p className="text-sm text-red-700">Xóa vĩnh viễn nhà hàng và tất cả dữ liệu</p>
            </div>
            <button className="px-4 py-2 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 transition-colors">
              Xóa vĩnh viễn
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold text-gray-900">Dashboard Nhà hàng</h1>
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                ✓ Hoạt động
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <RefreshCw className="w-5 h-5" />
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors">
                👁️ Xem trang công khai
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => {
                const IconComponent = tab.icon;
                return (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key)}
                    className={`
                      py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 transition-colors
                      ${activeTab === tab.key
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <IconComponent className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'overview' && <OverviewTab />}
          {activeTab === 'reviews' && <ReviewsTab />}
          {activeTab === 'analytics' && <AnalyticsTab />}
          {activeTab === 'settings' && <SettingsTab />}
        </div>
      </div>
    </div>
  );
};

export default RestaurantDashboard;