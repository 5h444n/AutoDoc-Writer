import { useEffect, useState } from 'react';
import axios from 'axios';
import { History, CheckCircle2, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';

interface HistoryItem {
    id: string;
    repo_name: string;
    style: string;
    timestamp: string;
    status: string;
}

export function HistoryView() {
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchHistory = async () => {
        try {
            const token = localStorage.getItem('access_token');
            // Assuming the endpoint is aligned with the file path I edited
            const response = await axios.get('http://localhost:8000/api/v1/ai/history', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHistory(response.data || []);
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch history:", err);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
        const interval = setInterval(fetchHistory, 2000); // Poll every 2s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="bg-[#111] rounded-xl border border-white/5 overflow-hidden h-full flex flex-col">
            <div className="p-4 border-b border-white/5 bg-white/5 flex items-center justify-between">
                <h3 className="font-semibold text-white flex items-center gap-2">
                    <History className="w-4 h-4 text-violet-500" />
                    Activity Feed
                </h3>
                <button onClick={fetchHistory} className="p-1 hover:bg-white/10 rounded-full transition-colors">
                    <RefreshCw className="w-4 h-4 text-gray-400" />
                </button>
            </div>

            <div className="flex-1 overflow-auto p-0 scrollbar-hide">
                {history.length === 0 ? (
                    <div className="p-8 text-center text-gray-500 text-sm">
                        No activity yet.
                    </div>
                ) : (
                    <div className="divide-y divide-white/5">
                        {history.map((item) => (
                            <div key={item.id} className="p-4 hover:bg-white/5 transition-colors animate-in slide-in-from-left-2 duration-300">
                                <div className="flex items-start justify-between mb-1">
                                    <span className="text-sm font-medium text-gray-200 truncate max-w-[180px]" title={item.repo_name}>
                                        {item.repo_name.replace('https://github.com/', '')}
                                    </span>
                                    <span className="bg-green-500/10 text-green-400 text-xs px-2 py-0.5 rounded-full flex items-center gap-1">
                                        <CheckCircle2 className="w-3 h-3" />
                                        {item.status}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between text-xs text-gray-500">
                                    <span className="capitalize bg-white/5 px-1.5 py-0.5 rounded text-gray-400">
                                        {item.style}
                                    </span>
                                    <span>
                                        {format(new Date(item.timestamp), 'h:mm a')}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
