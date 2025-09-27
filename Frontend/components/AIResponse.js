// AI Response Component
window.AIResponse = ({ response, restaurants }) => (
    <div className="ai-chat-bubble bg-white rounded-xl p-6 shadow-lg mb-8">
        <div className="flex items-center mb-4">
            <i className="fas fa-robot text-2xl text-blue-600 mr-3"></i>
            <h3 className="text-lg font-semibold text-gray-800">Gợi ý từ AI Assistant</h3>
        </div>

        <div className="prose prose-blue max-w-none">
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {response}
            </div>
        </div>

        {restaurants && restaurants.length > 0 && (
            <div className="mt-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">
                    <i className="fas fa-star text-yellow-500 mr-2"></i>
                    Nhà hàng được gợi ý
                </h4>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {restaurants.map((restaurant, index) => (
                        <window.RestaurantCard key={restaurant.id || index} restaurant={restaurant} />
                    ))}
                </div>
            </div>
        )}
    </div>
);