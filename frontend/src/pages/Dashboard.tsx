
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Loader2, RefreshCw, Plus, Wand2, Copy, Download, FileCode, FileText, BookOpen, CheckCircle2, X, Star } from 'lucide-react';
import { Toaster, toast } from 'sonner';
import { jsPDF } from 'jspdf';
import { Sidebar } from '../components/Sidebar';
import { RepoCard } from '../components/RepoCard';
import { RepoStats } from '../components/RepoStats';
import { ImportModal } from '../components/ImportModal';
import { HistoryView } from '../components/HistoryView';
import { AboutView } from '../components/AboutView';
import { SettingsView } from '../components/SettingsView';
import { GlassCard } from '../components/ui/GlassCard';
import { GlowButton } from '../components/ui/GlowButton';

export default function Dashboard() {
    const [githubRepos, setGithubRepos] = useState<any[]>([]);
    const [manualRepos, setManualRepos] = useState<any[]>([]);
    const [selectedRepo, setSelectedRepo] = useState<any | null>(null);
    const [activeView, setActiveView] = useState<'repos' | 'documents' | 'history' | 'about' | 'settings'>('repos');
    const [loading, setLoading] = useState(true);
    const [showImport, setShowImport] = useState(false);
    const [settings, setSettings] = useState({ displayName: 'User', language: 'English', model: 'gemini-2.0-flash-lite', temperature: 0.7, apiKey: '' });
    const [user, setUser] = useState<any>(null);

    // QoL State
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [pinnedRepos, setPinnedRepos] = useState<number[]>([]);
    const [savedDocs, setSavedDocs] = useState<any[]>([]);

    // QoL Load Effects
    useEffect(() => {
        const savedPinned = localStorage.getItem('pinned_repos');
        if (savedPinned) setPinnedRepos(JSON.parse(savedPinned));

        const savedDocsValid = localStorage.getItem('saved_docs');
        if (savedDocsValid) setSavedDocs(JSON.parse(savedDocsValid));
    }, []);

    const togglePin = (id: number) => {
        setPinnedRepos(prev => {
            const newPinned = prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id];
            localStorage.setItem('pinned_repos', JSON.stringify(newPinned));
            return newPinned;
        });
    };

    const sortedRepos = [...githubRepos].sort((a, b) => {
        const isAPinned = pinnedRepos.includes(a.id);
        const isBPinned = pinnedRepos.includes(b.id);
        if (isAPinned && !isBPinned) return -1;
        if (!isAPinned && isBPinned) return 1;
        return 0;
    });


    // Generation State
    const [selectedFormats, setSelectedFormats] = useState<string[]>(['markdown']);
    const [activePreviewTab, setActivePreviewTab] = useState<'markdown' | 'latex' | 'pdf'>('markdown');
    const [generatedDoc, setGeneratedDoc] = useState('');
    const [customInstructions, setCustomInstructions] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    // Load Repos Function (Fixes 401 Error)
    const fetchRepos = async () => {
        setLoading(true);
        const token = localStorage.getItem('github_token');

        // 1. Fetch GitHub Repos (if token exists)
        if (token) {
            try {
                const res = await axios.get('http://localhost:8000/api/v1/github/repos', {
                    headers: { Authorization: `Bearer ${token}` } // <--- CRITICAL FIX
                });
                setGithubRepos(res.data);
            } catch (error) {
                console.error("Failed to fetch GitHub repos", error);
                toast.error("Could not sync GitHub repositories.");
            }
        }
        setLoading(false);
    };

    // Initial Load
    useEffect(() => { fetchRepos(); }, []);

    // Fetch User Profile
    useEffect(() => {
        const token = localStorage.getItem('github_token');
        if (token) {
            axios.get('http://localhost:8000/api/v1/github/user', {
                headers: { Authorization: `Bearer ${token}` }
            }).then(res => setUser(res.data)).catch(err => console.error(err));
        }
    }, []);

    // Handle Import Logic
    const handleImport = (repo: any, type: 'github' | 'manual') => {
        if (type === 'github') {
            // Move from list to selection (or just select it)
            setSelectedRepo(repo);
            toast.success(`Selected ${repo.name}`);
        } else {
            // Add manual repo
            const newRepo = { ...repo, id: Date.now(), language: 'Manual', size: 0, open_issues_count: 0 };
            setManualRepos([newRepo, ...manualRepos]);
            toast.success('Repository imported manually');
        }
        setShowImport(false);
    };

    const downloadFile = (filename: string, content: string) => {
        const element = document.createElement("a");
        const file = new Blob([content], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = filename;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const handleLogout = () => {
        localStorage.removeItem('github_token');
        window.location.href = '/login';
    };

    const toggleFormat = (fmt: string) => {
        setSelectedFormats(prev =>
            prev.includes(fmt) ? prev.filter(f => f !== fmt) : [...prev, fmt]
        );
    };

    const getPreviewContent = () => {
        if (activePreviewTab === 'latex') {
            return `\\documentclass{article}\n\\usepackage{hyperref}\n\\begin{document}\n\n${generatedDoc}\n\n\\end{document}`;
        }
        return generatedDoc; // Markdown and PDF (text view) share the same source text
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(getPreviewContent());
        toast.success('Copied to clipboard');
    };

    const handleDownloadCurrent = () => {
        if (activePreviewTab === 'pdf') {
            const doc = new jsPDF();
            doc.setFontSize(10);
            const splitText = doc.splitTextToSize(generatedDoc, 180);
            doc.text(splitText, 10, 10);
            doc.save(`${selectedRepo.name}-report.pdf`);
        } else if (activePreviewTab === 'latex') {
            downloadFile(`${selectedRepo.name}.tex`, getPreviewContent());
        } else {
            downloadFile(`${selectedRepo.name}.md`, generatedDoc);
        }
        toast.success(`Downloaded ${activePreviewTab.toUpperCase()} file`);
    };

    const handleGenerate = async () => {
        if (!selectedRepo) return;
        setIsGenerating(true);
        setGeneratedDoc(''); // Clear previous

        try {
            // Use the real backend endpoint
            const response = await axios.post('http://localhost:8000/api/v1/ai/generate', {
                repo_url: selectedRepo.html_url || selectedRepo.url,
                style: 'Detailed', // Defaulting style for now
                settings: settings,
                custom_instructions: customInstructions,
                instructions: `IMPORTANT: Please write the documentation in ${settings.language}.`
            });

            setGeneratedDoc(response.data.documentation);

            // Auto-Save to Vault
            const newDoc = {
                id: Date.now(),
                repoName: selectedRepo.name,
                content: response.data.documentation,
                date: new Date().toLocaleString()
            };
            setSavedDocs(prev => {
                const updated = [newDoc, ...prev];
                localStorage.setItem('saved_docs', JSON.stringify(updated));
                return updated;
            });

            toast.success('Documentation generated and saved to Vault!');

        } catch (error) {
            console.error(error);
            toast.error('Failed to generate documentation. Check backend console.');
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="flex h-screen bg-slate-950 text-slate-200 selection:bg-indigo-500/30 overflow-hidden">
            <Sidebar activeView={activeView} onNavigate={setActiveView} onLogout={handleLogout} user={user} isCollapsed={isCollapsed} toggleCollapse={() => setIsCollapsed(!isCollapsed)} />
            <main className={`flex-1 ${isCollapsed ? 'ml-20' : 'ml-64'} p-8 overflow-auto relative scrollbar-hide transition-all duration-300`}>
                {activeView === 'repos' && (
                    <div className="max-w-7xl mx-auto space-y-8">
                        {/* Header Area */}
                        <div className="flex justify-between items-center">
                            <div>
                                <h1 className="text-2xl font-bold">Your Repositories</h1>
                                <p className="text-slate-400">Manage and document your codebase</p>
                            </div>
                            <div className="flex gap-3">
                                <button onClick={fetchRepos} className="p-2 text-slate-400 hover:bg-white/5 rounded-lg">
                                    <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
                                </button>
                                <GlowButton
                                    onClick={() => setShowImport(true)}
                                    className="px-4 py-2 flex items-center gap-2"
                                >
                                    <Plus className="h-4 w-4" /> Import Repository
                                </GlowButton>
                            </div>
                        </div>
                        {/* SELECTED REPO VIEW */}
                        {selectedRepo ? (
                            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                                <button onClick={() => setSelectedRepo(null)} className="text-sm text-slate-400 hover:text-violet-400 mb-4 transition">
                                    ← Back to Dashboard
                                </button>
                                <RepoStats repo={selectedRepo} />
                                <GlassCard className="space-y-8 border-violet-500/20 bg-violet-900/10">
                                    <div className="flex justify-between items-center">
                                        <div>
                                            <h2 className="text-2xl font-bold text-white">Generate Documentation</h2>
                                            <p className="text-slate-400 mt-1">Select your target formats and let AI analyze the code.</p>
                                        </div>
                                        <button onClick={() => setSelectedRepo(null)} className="text-slate-400 hover:text-white">
                                            <X className="h-5 w-5" />
                                        </button>
                                    </div>

                                    <div className="bg-slate-900/50 p-4 rounded-xl border border-white/10 focus-within:ring-2 focus-within:ring-violet-500/50 transition-all">
                                        <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                                            Custom Instructions (Optional)
                                        </label>
                                        <textarea
                                            value={customInstructions}
                                            onChange={(e) => setCustomInstructions(e.target.value)}
                                            placeholder="e.g., 'Focus heavily on the API endpoints', 'Use a friendly tone', 'Ignore the testing folder'..."
                                            className="w-full bg-transparent border-none focus:ring-0 p-0 text-sm text-white placeholder:text-slate-600 min-h-[60px] resize-none"
                                        />
                                    </div>

                                    {/* Format Selection Grid */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        {[
                                            { id: 'markdown', label: 'Markdown', desc: 'Standard .md files', icon: FileCode },
                                            { id: 'pdf', label: 'PDF Report', desc: 'Formal report layout', icon: FileText },
                                            { id: 'latex', label: 'LaTeX', desc: 'Academic styling', icon: BookOpen },
                                        ].map((fmt) => (
                                            <div
                                                key={fmt.id}
                                                onClick={() => toggleFormat(fmt.id)}
                                                className={`relative p-6 rounded-xl border cursor-pointer transition-all duration-200 group ${selectedFormats.includes(fmt.id)
                                                    ? 'border-violet-500 bg-violet-600/20'
                                                    : 'border-white/10 hover:border-white/20 hover:bg-white/5'
                                                    }`}
                                            >
                                                <div className={`mb-4 p-3 rounded-lg w-fit ${selectedFormats.includes(fmt.id) ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white' : 'bg-slate-800 text-slate-400 group-hover:text-white'
                                                    }`}>
                                                    <fmt.icon className="h-6 w-6" />
                                                </div>
                                                <h3 className={`font-bold ${selectedFormats.includes(fmt.id) ? 'text-violet-400' : 'text-slate-200'}`}>
                                                    {fmt.label}
                                                </h3>
                                                <p className="text-sm text-slate-500 mt-1">{fmt.desc}</p>

                                                {/* Checkmark Badge */}
                                                {selectedFormats.includes(fmt.id) && (
                                                    <div className="absolute top-4 right-4 text-violet-400">
                                                        <CheckCircle2 className="h-5 w-5 fill-violet-500/20" />
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                    {/* Big Generate Button */}
                                    <GlowButton
                                        onClick={handleGenerate}
                                        disabled={isGenerating || selectedFormats.length === 0}
                                        className="w-full py-5 flex items-center justify-center gap-3"
                                    >
                                        {isGenerating ? (
                                            <>
                                                <Loader2 className="h-5 w-5 animate-spin text-indigo-200" />
                                                <span className="text-white">Processing {selectedRepo.name}...</span>
                                            </>
                                        ) : (
                                            <>
                                                <Wand2 className="h-5 w-5 text-indigo-200" />
                                                <span>Generate Selected Formats</span>
                                            </>
                                        )}
                                    </GlowButton>

                                    {/* Output Preview Area */}
                                    {generatedDoc && (
                                        <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700 border-t border-white/5 pt-8">
                                            <div className="flex justify-between items-end mb-4">
                                                {/* Tabs */}
                                                <div className="flex gap-2">
                                                    {['markdown', 'pdf', 'latex'].map((tab) => (
                                                        selectedFormats.includes(tab) && (
                                                            <button
                                                                key={tab}
                                                                onClick={() => setActivePreviewTab(tab as any)}
                                                                className={`px-4 py-2 rounded-t-lg text-sm font-bold transition-all ${activePreviewTab === tab
                                                                    ? 'bg-slate-800 text-white translate-y-[1px] border-t border-x border-white/10'
                                                                    : 'bg-slate-900/50 text-slate-500 hover:text-slate-300'
                                                                    }`}
                                                            >
                                                                {tab.toUpperCase()}
                                                            </button>
                                                        )
                                                    ))}
                                                </div>
                                                {/* Action Buttons */}
                                                <div className="flex gap-2 mb-2">
                                                    <button
                                                        onClick={handleCopy}
                                                        className="p-2 text-slate-400 hover:bg-white/10 hover:text-white rounded-lg transition-colors"
                                                        title="Copy Content"
                                                    >
                                                        <Copy className="h-4 w-4" />
                                                    </button>
                                                    <button
                                                        onClick={handleDownloadCurrent}
                                                        className="p-2 text-slate-400 hover:bg-white/10 hover:text-white rounded-lg transition-colors"
                                                        title="Download File"
                                                    >
                                                        <Download className="h-4 w-4" />
                                                    </button>
                                                </div>
                                            </div>
                                            {/* Editor/Preview Window */}
                                            <div className="bg-gray-900 rounded-b-xl rounded-tr-xl overflow-hidden shadow-2xl">
                                                <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 border-b border-gray-700">
                                                    <div className="flex gap-1.5">
                                                        <div className="w-3 h-3 rounded-full bg-red-500" />
                                                        <div className="w-3 h-3 rounded-full bg-yellow-500" />
                                                        <div className="w-3 h-3 rounded-full bg-green-500" />
                                                    </div>
                                                    <span className="text-xs text-gray-400 font-mono ml-2">
                                                        {activePreviewTab === 'latex' ? 'source.tex' : activePreviewTab === 'pdf' ? 'preview.pdf' : 'README.md'}
                                                    </span>
                                                </div>
                                                <div className="p-6 overflow-auto max-h-[500px]">
                                                    <pre className="text-sm font-mono text-gray-300 whitespace-pre-wrap leading-relaxed">
                                                        {getPreviewContent()}
                                                    </pre>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </GlassCard>
                            </div>
                        ) : (
                            /* REPO LISTS */
                            <div className="space-y-8">
                                {/* GitHub Section */}
                                <section>
                                    <h2 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">From GitHub</h2>
                                    {githubRepos.length === 0 ? (
                                        <div className="p-8 border border-dashed border-white/10 rounded-xl text-center text-slate-500">
                                            {loading ? "Loading repositories..." : "No GitHub repositories found. Connect your account!"}
                                        </div>
                                    ) : (
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                            {sortedRepos.map((repo, i) => (
                                                <GlassCard delay={i * 0.05} key={repo.id} onClick={() => setSelectedRepo(repo)} className="cursor-pointer hover:bg-white/5 relative group">
                                                    <button
                                                        onClick={(e) => { e.stopPropagation(); togglePin(repo.id); }}
                                                        className={`absolute top-4 right-4 z-20 p-1.5 rounded-full transition-all ${pinnedRepos.includes(repo.id) ? 'bg-yellow-500/20 text-yellow-400' : 'bg-transparent text-slate-600 hover:bg-white/10 hover:text-yellow-400'}`}
                                                    >
                                                        <Star className={`w-4 h-4 ${pinnedRepos.includes(repo.id) ? 'fill-yellow-400' : ''}`} />
                                                    </button>
                                                    <RepoCard
                                                        name={repo.name}
                                                        description={repo.description}
                                                        html_url={repo.url || repo.html_url}
                                                        stargazers_count={repo.stargazers_count}
                                                        // repo={repo} // RepoCard logic from previous steps used flat props
                                                        isSelected={false}
                                                        onClick={() => setSelectedRepo(repo)}
                                                    />
                                                </GlassCard>
                                            ))}
                                        </div>
                                    )}
                                </section>
                                {/* Manual Section */}
                                {manualRepos.length > 0 && (
                                    <section>
                                        <div className="flex items-center gap-4 mb-4">
                                            <h2 className="text-sm font-bold text-slate-400 uppercase tracking-wider">External Imports</h2>
                                            <div className="h-px bg-white/10 flex-1" />
                                        </div>
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                            {manualRepos.map((repo, i) => (
                                                <GlassCard delay={i * 0.05} key={repo.id} onClick={() => setSelectedRepo(repo)} className="cursor-pointer hover:bg-white/5">
                                                    <RepoCard
                                                        name={repo.name}
                                                        description={repo.description}
                                                        html_url={repo.url}
                                                        stargazers_count={0}
                                                        isSelected={false}
                                                        onClick={() => setSelectedRepo(repo)}
                                                    />
                                                </GlassCard>
                                            ))}
                                        </div>
                                    </section>
                                )}
                            </div>
                        )}
                    </div>
                )}
                {activeView === 'documents' && (
                    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
                        <h2 className="text-3xl font-bold text-white flex items-center gap-2">
                            <FileText className="h-8 w-8 text-violet-400" />
                            My Saved Documents
                        </h2>
                        {savedDocs.length === 0 ? (
                            <div className="p-10 border border-dashed border-white/10 rounded-xl text-center text-slate-500">
                                No documents saved yet. Generate one to see it here!
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {savedDocs.map(doc => (
                                    <GlassCard key={doc.id} className="flex flex-col gap-4 border-violet-500/10 hover:border-violet-500/30">
                                        <div>
                                            <h3 className="font-bold text-white text-lg">{doc.repoName}</h3>
                                            <p className="text-xs text-violet-300/60 mt-1 font-mono">{doc.date}</p>
                                        </div>
                                        <div className="mt-auto flex gap-2 pt-4">
                                            <GlowButton onClick={() => downloadFile(`${doc.repoName}.md`, doc.content)} className="w-full text-sm py-2 group">
                                                <Download className="w-4 h-4 group-hover:animate-bounce" />
                                                Download
                                            </GlowButton>
                                        </div>
                                    </GlassCard>
                                ))}
                            </div>
                        )}
                    </div>
                )}
                {activeView === 'history' && <HistoryView />}
                {activeView === 'about' && <AboutView onClose={() => setActiveView('repos')} />}
                {activeView === 'settings' && <SettingsView settings={settings} onSave={setSettings} />}
                {
                    showImport && (
                        <ImportModal
                            onClose={() => setShowImport(false)}
                            onImport={handleImport}
                        />
                    )
                }
            </main >
            <Toaster position="bottom-right" richColors />
        </div >
    );
}
