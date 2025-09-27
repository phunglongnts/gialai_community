// ===== APPLICATION INITIALIZATION =====

// Loading Screen Management
class LoadingManager {
    constructor() {
        this.loadingScreen = document.getElementById('loading-screen');
        this.isLoaded = false;
    }

    show() {
        if (this.loadingScreen) {
            this.loadingScreen.style.display = 'flex';
            this.loadingScreen.style.opacity = '1';
        }
    }

    hide() {
        if (this.loadingScreen && !this.isLoaded) {
            this.isLoaded = true;
            this.loadingScreen.style.opacity = '0';
            this.loadingScreen.style.transition = 'opacity 0.5s ease-out';

            setTimeout(() => {
                this.loadingScreen.style.display = 'none';
                this.onLoadingComplete();
            }, 500);
        }
    }

    onLoadingComplete() {
        // Trigger custom event when loading is complete
        const event = new CustomEvent('appLoaded', {
            detail: { timestamp: Date.now() }
        });
        window.dispatchEvent(event);
        console.log('✅ Application loaded successfully');
    }
}

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.initializeTheme();
    }

    getStoredTheme() {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.THEME);
    }

    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, theme);
        document.documentElement.setAttribute('data-theme', theme);

        // Update meta theme-color for mobile browsers
        const themeColorMeta = document.querySelector('meta[name="theme-color"]');
        if (themeColorMeta) {
            themeColorMeta.content = theme === 'dark' ? '#1e293b' : '#ffffff';
        }
    }

    initializeTheme() {
        this.setTheme(this.currentTheme);
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        return newTheme;
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            apiCalls: []
        };
        this.startTime = performance.now();
    }

    recordLoadTime() {
        this.metrics.loadTime = performance.now() - this.startTime;
        console.log(`📊 App load time: ${this.metrics.loadTime.toFixed(2)}ms`);
    }

    recordAPICall(endpoint, duration, status) {
        this.metrics.apiCalls.push({
            endpoint,
            duration,
            status,
            timestamp: Date.now()
        });
    }

    getMetrics() {
        return {
            ...this.metrics,
            averageAPITime: this.getAverageAPITime()
        };
    }

    getAverageAPITime() {
        if (this.metrics.apiCalls.length === 0) return 0;
        const total = this.metrics.apiCalls.reduce((sum, call) => sum + call.duration, 0);
        return total / this.metrics.apiCalls.length;
    }
}

// Error Handler
class GlobalErrorHandler {
    constructor() {
        this.setupErrorHandlers();
    }

    setupErrorHandlers() {
        // Handle JavaScript errors
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'javascript',
                message: event.message,
                source: event.filename,
                line: event.lineno,
                column: event.colno,
                stack: event.error?.stack
            });
        });

        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'promise',
                message: event.reason?.message || 'Unhandled promise rejection',
                stack: event.reason?.stack
            });
            event.preventDefault();
        });

        // Handle React errors (if available)
        if (typeof React !== 'undefined' && React.version) {
            console.log(`⚛️  React version: ${React.version}`);
        }
    }

    handleError(errorInfo) {
        console.error('🚨 Global Error:', errorInfo);

        // Show user-friendly error message
        this.showErrorToast(errorInfo);

        // Send to analytics (if enabled)
        if (CONFIG.FEATURES.ENABLE_ANALYTICS) {
            this.reportError(errorInfo);
        }
    }

    showErrorToast(errorInfo) {
        const toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 max-w-sm';
        toast.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                <div>
                    <div class="font-semibold">Có lỗi xảy ra</div>
                    <div class="text-sm opacity-90">Vui lòng tải lại trang</div>
                </div>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    reportError(errorInfo) {
        // Placeholder for error reporting service
        // Could integrate with services like Sentry, LogRocket, etc.
        console.log('📊 Error reported:', errorInfo);
    }
}

// App Initializer
class AppInitializer {
    constructor() {
        this.loadingManager = new LoadingManager();
        this.themeManager = new ThemeManager();
        this.performanceMonitor = new PerformanceMonitor();
        this.errorHandler = new GlobalErrorHandler();

        this.init();
    }

    async init() {
        try {
            console.log('🚀 Initializing Gia Lai Community App...');

            // Show loading screen
            this.loadingManager.show();

            // Wait for DOM to be ready
            await this.waitForDOM();

            // Initialize components
            await this.initializeComponents();

            // Setup global event listeners
            this.setupGlobalListeners();

            // Hide loading screen after minimum duration
            setTimeout(() => {
                this.loadingManager.hide();
                this.performanceMonitor.recordLoadTime();
            }, CONFIG.UI.LOADING_SCREEN_DURATION);

        } catch (error) {
            console.error('❌ App initialization failed:', error);
            this.errorHandler.handleError({
                type: 'initialization',
                message: error.message,
                stack: error.stack
            });
        }
    }

    waitForDOM() {
        return new Promise((resolve) => {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', resolve);
            } else {
                resolve();
            }
        });
    }

    async initializeComponents() {
        // Preload critical resources
        await this.preloadResources();

        // Initialize local storage
        this.initializeStorage();

        // Setup service worker (if supported)
        if (CONFIG.FEATURES.ENABLE_OFFLINE_MODE) {
            this.registerServiceWorker();
        }

        // Initialize analytics
        if (CONFIG.FEATURES.ENABLE_ANALYTICS) {
            this.initializeAnalytics();
        }
    }

    async preloadResources() {
        const resources = [
            // Preload critical images
            'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🍜</text></svg>',
        ];

        const promises = resources.map(url => {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = resolve;
                img.onerror = resolve; // Don't fail on image errors
                img.src = url;
            });
        });

        await Promise.allSettled(promises);
        console.log('📦 Resources preloaded');
    }

    initializeStorage() {
        // Initialize default values in localStorage
        const defaults = {
            [CONFIG.STORAGE_KEYS.SEARCH_HISTORY]: [],
            [CONFIG.STORAGE_KEYS.USER_PREFERENCES]: {
                language: 'vi',
                notifications: true,
                darkMode: false
            },
            [CONFIG.STORAGE_KEYS.FAVORITES]: []
        };

        Object.entries(defaults).forEach(([key, defaultValue]) => {
            if (!localStorage.getItem(key)) {
                localStorage.setItem(key, JSON.stringify(defaultValue));
            }
        });

        console.log('💾 Local storage initialized');
    }

    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('✅ Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('❌ Service Worker registration failed:', error);
                });
        }
    }

    initializeAnalytics() {
        // Placeholder for analytics initialization
        console.log('📊 Analytics initialized');

        // Track page load
        this.trackEvent('page_load', {
            page: 'home',
            timestamp: Date.now(),
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`
        });
    }

    trackEvent(eventName, properties = {}) {
        if (!CONFIG.FEATURES.ENABLE_ANALYTICS) return;

        console.log('📊 Analytics Event:', eventName, properties);
        // Here you would send to your analytics service
    }

    setupGlobalListeners() {
        // Handle app loaded event
        window.addEventListener('appLoaded', (event) => {
            console.log('🎉 App fully loaded at:', new Date(event.detail.timestamp));
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            console.log('🌐 App is online');
            this.showNetworkStatus('online');
        });

        window.addEventListener('offline', () => {
            console.log('📴 App is offline');
            this.showNetworkStatus('offline');
        });

        // Handle visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                console.log('👀 App became visible');
            } else {
                console.log('😴 App became hidden');
            }
        });

        // Handle before unload
        window.addEventListener('beforeunload', (event) => {
            // Clean up any pending operations
            this.cleanup();
        });
    }

    showNetworkStatus(status) {
        const existingStatus = document.querySelector('.network-status');
        if (existingStatus) existingStatus.remove();

        const statusEl = document.createElement('div');
        statusEl.className = `network-status fixed top-4 left-1/2 transform -translate-x-1/2 px-4 py-2 rounded-full text-white text-sm font-medium z-50 ${
            status === 'online' ? 'bg-green-500' : 'bg-red-500'
        }`;
        statusEl.innerHTML = `
            <i class="fas fa-${status === 'online' ? 'wifi' : 'wifi-slash'} mr-2"></i>
            ${status === 'online' ? 'Đã kết nối internet' : 'Mất kết nối internet'}
        `;

        document.body.appendChild(statusEl);

        setTimeout(() => {
            if (statusEl.parentElement) {
                statusEl.remove();
            }
        }, 3000);
    }

    cleanup() {
        // Clean up any pending operations, timers, etc.
        console.log('🧹 Cleaning up app resources');
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.appInitializer = new AppInitializer();
});

// Make classes available globally
window.LoadingManager = LoadingManager;
window.ThemeManager = ThemeManager;
window.PerformanceMonitor = PerformanceMonitor;
window.GlobalErrorHandler = GlobalErrorHandler;