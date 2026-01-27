import { Layout, Settings, LogOut, History, Info, FileText, ChevronLeft, ChevronRight } from 'lucide-react';

interface SidebarProps {
    activeView?: 'repos' | 'documents' | 'history' | 'about' | 'settings';
    onNavigate?: (view: 'repos' | 'documents' | 'history' | 'about' | 'settings') => void;
    onLogout?: () => void;
    user?: any;
    isCollapsed: boolean;
    toggleCollapse: () => void;
}

export function Sidebar({ activeView = 'repos', onNavigate, onLogout, user, isCollapsed, toggleCollapse }: SidebarProps) {
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        window.location.reload();
    };

    return (
        <div className={`${isCollapsed ? 'w-20' : 'w-64'} h-screen bg-slate-900/50 backdrop-blur-2xl border-r border-white/5 text-white flex flex-col fixed left-0 top-0 transition-all duration-300 z-50`}>
            {/* Header */}
            <div className="p-6 border-b border-gray-800 flex justify-between items-center relative">
                {!isCollapsed && (
                    <h1 className="text-xl font-bold flex items-center gap-2 animate-in fade-in duration-300">
                        <Layout className="w-6 h-6" />
                        AutoDoc
                    </h1>
                )}
                {isCollapsed && <Layout className="w-6 h-6 mx-auto" />}

                <button
                    onClick={toggleCollapse}
                    className="absolute -right-3 top-6 bg-slate-800 border border-white/10 rounded-full p-1 text-slate-400 hover:text-white transition-colors shadow-lg"
                >
                    {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
                </button>
            </div>

            {/* Nav Items */}
            <div className="py-4 space-y-2 px-3">
                {[
                    { id: 'repos', label: 'Repositories', icon: Layout },
                    { id: 'documents', label: 'My Documents', icon: FileText },
                    { id: 'history', label: 'History', icon: History },
                    { id: 'about', label: 'About', icon: Info },
                    { id: 'settings', label: 'Settings', icon: Settings }
                ].map((item) => (
                    <button
                        key={item.id}
                        onClick={() => onNavigate?.(item.id as any)}
                        className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-300 group ${activeView === item.id
                            ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-[0_0_20px_rgba(99,102,241,0.5)]'
                            : 'text-gray-400 hover:text-white hover:bg-white/5'
                            } ${isCollapsed ? 'justify-center' : ''}`}
                        title={isCollapsed ? item.label : undefined}
                    >
                        <item.icon className={`w-5 h-5 flex-shrink-0 ${activeView === item.id ? 'text-white' : 'text-gray-500 group-hover:text-white'}`} />
                        {!isCollapsed && <span className="font-semibold whitespace-nowrap">{item.label}</span>}
                    </button>
                ))}
            </div>

            {/* Footer / Profile */}
            <div className="p-4 border-t border-white/5 mt-auto">
                <div className="pt-4">
                    {user ? (
                        <button
                            onClick={onLogout}
                            className={`flex items-center gap-3 w-full p-2 rounded-xl bg-[#111] border border-white/5 hover:bg-white/10 transition-all group ${isCollapsed ? 'justify-center' : ''}`}
                        >
                            <img
                                src={user.avatar_url}
                                alt="User"
                                className="w-10 h-10 rounded-full border border-gray-700 block"
                            />
                            {!isCollapsed && (
                                <>
                                    <div className="flex-1 text-left min-w-0">
                                        <p className="text-sm font-bold text-white truncate">{user.name || user.login}</p>
                                        <p className="text-xs text-gray-500 truncate">@{user.login}</p>
                                    </div>
                                    <LogOut className="h-4 w-4 text-gray-500 group-hover:text-red-400 transition-colors" />
                                </>
                            )}
                        </button>
                    ) : (
                        <button onClick={onLogout} className={`flex items-center gap-3 w-full p-3 text-slate-400 hover:text-white ${isCollapsed ? 'justify-center' : ''}`}>
                            <LogOut className="h-5 w-5" />
                            {!isCollapsed && <span className="font-medium">Log Out</span>}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
