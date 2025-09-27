// Restaurant Card Component
window.RestaurantCard = ({ restaurant }) => {
    const renderStars = (rating) => {
        const stars = [];
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;

        for (let i = 0; i < fullStars; i++) {
            stars.push(<i key={i} className="fas fa-star rating-stars"></i>);
        }

        if (hasHalfStar) {
            stars.push(<i key="half" className="fas fa-star-half-alt rating-stars"></i>);
        }

        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            stars.push(<i key={`empty-${i}`} className="far fa-star rating-stars"></i>);
        }

        return stars;
    };

    const getPriceDisplay = (priceRange, averagePrice) => {
        const ranges = {
            'budget': '💰',
            'mid-range': '💰💰',
            'high-end': '💰💰💰'
        };

        let display = ranges[priceRange] || '💰';
        if (averagePrice) {
            display += ` ~${averagePrice.toLocaleString('vi-VN')}đ`;
        }
        return display;
    };

    return (
        <div className="restaurant-card rounded-xl p-6 card-hover">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-1">{restaurant.name}</h3>
                    <div className="flex items-center space-x-2 text-gray-600">
                        <i className="fas fa-tag"></i>
                        <span>{restaurant.category}</span>
                    </div>
                </div>
                <div className="text-right">
                    <div className="flex items-center space-x-1 mb-1">
                        {renderStars(restaurant.average_rating || 0)}
                        <span className="text-gray-700 font-semibold ml-2">
                            {(restaurant.average_rating || 0).toFixed(1)}
                        </span>
                    </div>
                    <div className="text-sm text-gray-500">
                        {restaurant.total_reviews || 0} đánh giá
                    </div>
                </div>
            </div>

            <p className="text-gray-600 mb-4 line-clamp-2">
                {restaurant.description || 'Nhà hàng chất lượng với thực đơn đa dạng'}
            </p>

            <div className="space-y-2 mb-4">
                <div className="flex items-center text-gray-700">
                    <i className="fas fa-map-marker-alt w-5 text-red-500"></i>
                    <span className="ml-2 text-sm">{restaurant.address}</span>
                </div>

                {restaurant.phone && (
                    <div className="flex items-center text-gray-700">
                        <i className="fas fa-phone w-5 text-green-500"></i>
                        <span className="ml-2 text-sm">{restaurant.phone}</span>
                    </div>
                )}

                <div className="flex items-center text-gray-700">
                    <i className="fas fa-dollar-sign w-5 text-yellow-500"></i>
                    <span className="ml-2 text-sm">
                        {getPriceDisplay(restaurant.price_range, restaurant.average_price)}
                    </span>
                </div>
            </div>

            {restaurant.cuisine_types && restaurant.cuisine_types.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                    {restaurant.cuisine_types.slice(0, 3).map((cuisine, index) => (
                        <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                            {cuisine}
                        </span>
                    ))}
                </div>
            )}

            {restaurant.features && restaurant.features.length > 0 && (
                <div className="flex flex-wrap gap-2">
                    {restaurant.features.slice(0, 4).map((feature, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            <i className="fas fa-check-circle text-green-500 mr-1"></i>
                            {feature}
                        </span>
                    ))}
                </div>
            )}
        </div>
    );
};