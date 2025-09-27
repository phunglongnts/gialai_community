// AI Search Component
window.AISearch = ({ onSearchResult }) => {
    const { useState } = React;
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsLoading(true);
        setError('');

        try {
            const response = await window.api.post('/ai/search', {
                query: query.trim()
            });

            onSearchResult(response.data);
        } catch (err) {
            setError(window.AppConfig.MESSAGES.SEARCH_ERROR);
            console.error('Search error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="search-container rounded-xl p-6 shadow-lg mb-8">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                    <i className="fas fa-search-location mr-2 text-blue-600"></i>
                    Tìm kiếm nhà hàng với AI
                </h2>
                <p className="text-gray-600">{window.AppConfig.MESSAGES.SEARCH_DESCRIPTION}</p>
            </div>

            <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder={window.AppConfig.MESSAGES.SEARCH_PLACEHOLDER}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                        disabled={isLoading}
                    />
                </div>
                <button
                    type="submit"
                    disabled={isLoading || !query.trim()}
                    className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-colors"
                >
                    {isLoading ? (
                        <span className="ai-thinking">
                            <i className="fas fa-robot mr-2"></i>
                            {window.AppConfig.MESSAGES.AI_THINKING}
                        </span>
                    ) : (
                        <>
                            <i className="fas fa-search mr-2"></i>
                            Tìm kiếm
                        </>
                    )}
                </button>
            </form>

            {error && (
                <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                    <i className="fas fa-exclamation-triangle mr-2"></i>
                    {error}
                </div>
            )}
        </div>
    );
};