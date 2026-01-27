import { useState } from 'react';
import { User, Cpu, Globe, Key, Trash2, Save, Settings } from 'lucide-react';
import { toast } from 'sonner';
import { GlassCard } from './ui/GlassCard';
import { GlowButton } from './ui/GlowButton';

interface SettingsProps {
    settings: {
        displayName: string;
        model: string;
        temperature: number;
        language: string;
        apiKey: string;
    };
    onSave: (settings: any) => void;
}

export function SettingsView({ settings, onSave }: SettingsProps) {
    const [displayName, setDisplayName] = useState(settings.displayName);
    const [model, setModel] = useState(settings.model);
    const [temperature, setTemperature] = useState(settings.temperature);
    const [language, setLanguage] = useState(settings.language);
    const [apiKey, setApiKey] = useState(settings.apiKey);

    const handleSave = () => {
        onSave({ displayName, model, temperature, language, apiKey });
        toast.success("Settings saved successfully!");
    };

    const handleClearHistory = () => {
        if (confirm("Are you sure you want to clear all generation history? This cannot be undone.")) {
            // Placeholder for clear history logic
            toast.success("History cleared!");
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500 pb-10">
            <header>
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <Settings className="w-6 h-6 text-blue-400" />
                    Settings
                </h2>
                <p className="text-slate-400 mt-1">Manage your profile and AI configuration.</p>
            </header>

            {/* Profile Settings */}
            <GlassCard className="p-0 overflow-hidden border-blue-500/20 bg-blue-900/10">
                <div className="p-6 border-b border-white/5 bg-white/5">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <User className="w-4 h-4 text-blue-400" />
                        Profile Settings
                    </h3>
                </div>
                <div className="p-6">
                    <label className="block text-sm font-medium text-slate-300 mb-2">Display Name</label>
                    <input
                        type="text"
                        value={displayName}
                        onChange={(e) => setDisplayName(e.target.value)}
                        className="w-full max-w-md p-2.5 bg-slate-900/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500/50 outline-none text-white placeholder:text-slate-600"
                    />
                    <p className="text-xs text-slate-500 mt-2">
                        This name will appear in the History timeline and generated reports.
                    </p>
                </div>
            </GlassCard>

            {/* AI Preferences */}
            <GlassCard className="p-0 overflow-hidden border-purple-500/20 bg-purple-900/5">
                <div className="p-6 border-b border-white/5 bg-white/5">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-purple-400" />
                        AI Preferences
                    </h3>
                </div>
                <div className="p-6 space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">Model</label>
                            <select
                                value={model}
                                onChange={(e) => setModel(e.target.value)}
                                className="w-full p-2.5 bg-slate-900/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500/50 outline-none text-white"
                            >
                                <option value="gemini-2.0-flash-lite">Gemini 2.0 Flash Lite (Recommended)</option>
                                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                                <option value="gemini-ultra">Gemini Ultra</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">Output Language</label>
                            <div className="relative">
                                <Globe className="absolute left-3 top-3 w-4 h-4 text-slate-500" />
                                <select
                                    value={language}
                                    onChange={(e) => setLanguage(e.target.value)}
                                    className="w-full pl-10 p-2.5 bg-slate-900/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500/50 outline-none text-white"
                                >
                                    <option value="English">English</option>
                                    <option value="Spanish">Spanish</option>
                                    <option value="Bengali">Bengali</option>
                                    <option value="French">French</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-slate-300">Creativity (Temperature)</label>
                            <span className="text-sm text-slate-500">{temperature}</span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.1"
                            value={temperature}
                            onChange={(e) => setTemperature(parseFloat(e.target.value))}
                            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                        />
                        <div className="flex justify-between mt-1 text-xs text-slate-500">
                            <span>Precise</span>
                            <span>Creative</span>
                        </div>
                    </div>
                </div>
            </GlassCard>

            {/* Developer Settings */}
            <GlassCard className="p-0 overflow-hidden border-orange-500/20 bg-orange-900/5">
                <div className="p-6 border-b border-white/5 bg-white/5">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <Key className="w-4 h-4 text-orange-400" />
                        Developer Settings
                    </h3>
                </div>
                <div className="p-6 space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">API Key</label>
                        <input
                            type="password"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            className="w-full font-mono text-sm p-2.5 bg-slate-900/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500/50 outline-none text-white"
                        />
                    </div>

                    <div className="pt-4 border-t border-white/5">
                        <h4 className="text-sm font-medium text-red-400 mb-2">Danger Zone</h4>
                        <button
                            onClick={handleClearHistory}
                            className="flex items-center gap-2 px-4 py-2 border border-red-500/30 text-red-400 rounded-lg hover:bg-red-500/10 transition-colors text-sm font-medium"
                        >
                            <Trash2 className="w-4 h-4" />
                            Clear All Generation History
                        </button>
                    </div>
                </div>
            </GlassCard>

            {/* Save Button */}
            <div className="flex justify-end pt-4">
                <GlowButton
                    onClick={handleSave}
                    className="flex items-center gap-2 px-6 py-3"
                >
                    <Save className="w-5 h-5" />
                    Save Changes
                </GlowButton>
            </div>
        </div>
    );
}
