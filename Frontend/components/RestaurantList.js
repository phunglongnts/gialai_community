// Restaurant List Component
window.RestaurantList = () => {
    const { useState, useEffect } = React;
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchRestaurants = async () => {
            try {
                const response = await window.api.get('/restaurants/');
                setRestaurants(response.data);
            } catch (err) {
                setError('Không thể tải danh sách nhà hàng');
                console.error('Fetch restaurants error:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchRestaurants();
    }, []);

    if (loading) {
        return (
            <div className="text-center py-12">
                <i className="fas fa-spinner fa-spin text-4xl text-blue-600 mb-4"></i>
                <p className="text-gray-600">{window.AppConfig.MESSAGES.LOADING_RESTAURANTS}</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg">
                <i className="fas fa-exclamation-triangle mr-2"></i>
                {error}
            </div>
        );
    }

    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                    <i className="fas fa-utensils mr-2 text-orange-500"></i>
                    Tất cả nhà hàng ({restaurants.length})
                </h2>
            </div>

            {restaurants.length === 0 ? (
                <div className="text-center py-12 bg-white rounded-xl shadow-lg">
                    <i className="fas fa-store-slash text-6xl text-gray-300 mb-4"></i>
                    <p className="text-gray-500 text-lg">{window.AppConfig.MESSAGES.NO_RESTAURANTS}</p>
                    <p className="text-gray-400 text-sm mt-2">{window.AppConfig.MESSAGES.SETUP_INSTRUCTION}</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {restaurants.map((restaurant) => (
                        <window.RestaurantCard key={restaurant.id} restaurant={restaurant} />
                    ))}
                </div>
            )}
        </div>
    );
};