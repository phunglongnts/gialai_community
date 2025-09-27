// Status Indicator Component
window.StatusIndicator = () => {
    const { useState, useEffect } = React;
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const response = await window.api.get('/health');
                setStatus(response.data);
            } catch (err) {
                setStatus({ status: 'error', database: 'ERROR', llm: 'ERROR' });
            } finally {
                setLoading(false);
            }
        };

        checkStatus();
        const interval = setInterval(checkStatus, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) return null;

    return (
        <div className="status-indicator">
            <div className="text-sm">
                <div className="flex items-center space-x-2 mb-1">
                    <span className="text-gray-600">API:</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                        status?.status === 'running'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                    }`}>
                        {status?.status === 'running' ? 'ON' : 'OFF'}
                    </span>
                </div>
                <div className="flex items-center space-x-2 mb-1">
                    <span className="text-gray-600">DB:</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                        status?.database === 'OK'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                    }`}>
                        {status?.database}
                    </span>
                </div>
                <div className="flex items-center space-x-2">
                    <span className="text-gray-600">AI:</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                        status?.llm === 'OK'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                    }`}>
                        {status?.llm === 'OK' ? 'ON' : 'OFF'}
                    </span>
                </div>
            </div>
        </div>
    );
};