// Header Component
window.Header = () => {
    const handleAuthNavigation = () => {
        window.location.href = 'auth_components.html';
    };

    return (
        <header className="gradient-bg shadow-lg">
            <div className="container mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <i className="fas fa-utensils text-white text-3xl"></i>
                        <div>
                            <h1 className="text-white text-2xl font-bold">{window.AppConfig.SITE_TITLE}</h1>
                            <p className="text-blue-100 text-sm">{window.AppConfig.SITE_SUBTITLE}</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <button
                            onClick={handleAuthNavigation}
                            className="bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors shadow-md"
                        >
                            <i className="fas fa-sign-in-alt mr-2"></i>
                            Đăng nhập / Đăng ký
                        </button>
                        <div className="flex items-center space-x-2 text-white">
                            <i className="fas fa-robot text-2xl"></i>
                            <span className="hidden md:block">Trợ lý AI</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};