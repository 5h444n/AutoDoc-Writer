import { Layout, Settings, LogOut, History, Info } from 'lucide-react';

interface SidebarProps {
    activeView?: 'repos' | 'history' | 'about' | 'settings';
    onNavigate?: (view: 'repos' | 'history' | 'about' | 'settings') => void;
    onLogout?: () => void;
    user?: any;
}

export function Sidebar({ activeView = 'repos', onNavigate, onLogout, user }: SidebarProps) {
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        window.location.reload();
    };

    return (
        <div className="w-64 h-screen bg-slate-900/50 backdrop-blur-2xl border-r border-white/5 text-white flex flex-col fixed left-0 top-0">
            <div className="p-6 border-b border-gray-800">
                <h1 className="text-xl font-bold flex items-center gap-2">
                    <Layout className="w-6 h-6" />
                    AutoDoc
                </h1>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                <button
                    onClick={() => onNavigate?.('repos')}
                    className={`w-full flex items-center gap-3 px-4 py-2 rounded transition ${activeView === 'repos' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
                        }`}
                >
                    <Layout className="w-5 h-5" />
                    Repositories
                </button>

                <button
                    onClick={() => onNavigate?.('history')}
                    className={`w-full flex items-center gap-3 px-4 py-2 rounded transition ${activeView === 'history' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
                        }`}
                >
                    <History className="w-5 h-5" />
                    History
                </button>

                <button
                    onClick={() => onNavigate?.('about')}
                    className={`w-full flex items-center gap-3 px-4 py-2 rounded transition ${activeView === 'about' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
                        }`}
                >
                    <Info className="w-5 h-5" />
                    About
                </button>

                <button
                    onClick={() => onNavigate?.('settings')}
                    className={`w-full flex items-center gap-3 px-4 py-2 rounded transition ${activeView === 'settings' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
                        }`}
                >
                    <Settings className="w-5 h-5" />
                    Settings
                </button>
            </nav>

            <div className="p-4 border-t border-white/5">
                <div className="mt-auto border-t border-white/5 pt-4">
                    {user ? (
                        <button
                            onClick={onLogout}
                            className="flex items-center gap-3 w-full p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 transition-all group"
                        >
                            <img
                                src={user.avatar_url}
                                alt="User"
                                className="w-10 h-10 rounded-full border border-gray-700"
                            />
                            <div className="flex-1 text-left min-w-0">
                                <p className="text-sm font-bold text-white truncate">{user.name || user.login}</p>
                                <p className="text-xs text-gray-500 truncate">@{user.login}</p>
                            </div>
                            <LogOut className="h-4 w-4 text-gray-500 group-hover:text-red-400 transition-colors" />
                        </button>
                    ) : (
                        <button onClick={onLogout} className="flex items-center gap-3 w-full p-3 text-slate-400 hover:text-white">
                            <LogOut className="h-5 w-5" />
                            <span className="font-medium">Log Out</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
