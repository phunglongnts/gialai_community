// Main App Component
const App = () => {
    const { useState } = React;
    const [aiResponse, setAiResponse] = useState(null);
    const [searchResults, setSearchResults] = useState([]);

    const handleSearchResult = (result) => {
        setAiResponse(result.ai_response);
        setSearchResults(result.recommended_restaurants || []);
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <window.Header />

            <main className="container mx-auto px-6 py-8">
                <window.AISearch onSearchResult={handleSearchResult} />

                {aiResponse && (
                    <window.AIResponse
                        response={aiResponse}
                        restaurants={searchResults}
                    />
                )}

                <window.RestaurantList />
            </main>

            <window.StatusIndicator />

            <footer className="bg-gray-800 text-white py-8 mt-16">
                <div className="container mx-auto px-6 text-center">
                    <p>&copy; 2025 Cộng đồng Gia Lai. Powered by AI & FastAPI</p>
                </div>
            </footer>
        </div>
    );
};

// Render App
ReactDOM.render(<App />, document.getElementById('root'));