import { useState } from 'react';
import { X, Github, Code2 } from 'lucide-react';

interface ImportModalProps {
    onClose: () => void;
    onImport: (repo: any, type: 'github' | 'manual') => void;
}

export function ImportModal({ onClose, onImport }: ImportModalProps) {
    const [activeTab, setActiveTab] = useState<'github' | 'manual'>('github');
    const [manualName, setManualName] = useState('');
    const [manualDesc, setManualDesc] = useState('');

    const handleManualSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (manualName) {
            onImport({
                name: manualName,
                description: manualDesc,
                url: '#',
                language: 'Manual'
            }, 'manual');
        }
    };

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#0f0f0f] border border-white/10 rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
                <div className="p-4 border-b border-white/5 flex justify-between items-center bg-white/5">
                    <h3 className="font-semibold text-white">Import Repository</h3>
                    <button onClick={onClose} className="text-gray-400 hover:text-white">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                <div className="flex border-b border-white/5">
                    <button
                        onClick={() => setActiveTab('github')}
                        className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 border-b-2 transition-colors ${activeTab === 'github' ? 'border-violet-500 text-violet-400 bg-violet-500/10' : 'border-transparent text-gray-500 hover:text-white'}`}
                    >
                        <Github className="w-4 h-4" />
                        From GitHub
                    </button>
                    <button
                        onClick={() => setActiveTab('manual')}
                        className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 border-b-2 transition-colors ${activeTab === 'manual' ? 'border-violet-500 text-violet-400 bg-violet-500/10' : 'border-transparent text-gray-500 hover:text-white'}`}
                    >
                        <Code2 className="w-4 h-4" />
                        Manual Entry
                    </button>
                </div>

                <div className="p-6">
                    {activeTab === 'github' ? (
                        <div className="text-center py-8">
                            <p className="text-gray-400 mb-4">You can select GitHub repositories directly from your dashboard.</p>
                            <button
                                onClick={onClose}
                                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 font-medium"
                            >
                                Go to Dashboard
                            </button>
                        </div>
                    ) : (
                        <form onSubmit={handleManualSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Repository Name</label>
                                <input
                                    type="text"
                                    required
                                    value={manualName}
                                    onChange={(e) => setManualName(e.target.value)}
                                    placeholder="e.g. my-awesome-project"
                                    className="w-full p-2 bg-black/20 border border-white/10 text-white rounded-lg focus:ring-2 focus:ring-violet-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Description</label>
                                <textarea
                                    value={manualDesc}
                                    onChange={(e) => setManualDesc(e.target.value)}
                                    placeholder="Brief description of your project..."
                                    className="w-full p-2 bg-black/20 border border-white/10 text-white rounded-lg focus:ring-2 focus:ring-violet-500 outline-none h-24 resize-none"
                                />
                            </div>
                            <button
                                type="submit"
                                className="w-full py-2 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-lg hover:from-indigo-500 hover:to-violet-500 font-medium"
                            >
                                Import Repository
                            </button>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
}
