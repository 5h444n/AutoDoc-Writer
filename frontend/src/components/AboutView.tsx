import { X } from 'lucide-react';
import { GlassCard } from './ui/GlassCard';

export function AboutView({ onClose }: { onClose: () => void }) {
    return (
        <div className="flex flex-col items-center justify-center h-full animate-in fade-in duration-500 content-center justify-items-center">
            <GlassCard className="max-w-lg w-full text-center relative p-8">
                <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white">
                    <X className="h-5 w-5" />
                </button>

                <div className="h-16 w-16 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-xl mx-auto flex items-center justify-center mb-6 shadow-lg shadow-violet-500/30">
                    <span className="text-white text-2xl font-bold">Ad</span>
                </div>

                <h2 className="text-3xl font-bold text-white mb-2">AutoDoc Writer</h2>
                <p className="text-slate-400 mb-8">Intelligent Documentation Engine</p>

                <div className="space-y-4 text-left bg-[#0f0f0f]/50 p-6 rounded-xl border border-white/5">
                    <div className="flex justify-between">
                        <span className="text-slate-400 font-medium">Model</span>
                        <span className="font-bold text-slate-200">Gemini 2.0 Flash Lite</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-400 font-medium">Frontend</span>
                        <span className="font-bold text-slate-200">React + Tailwind</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-400 font-medium">Backend</span>
                        <span className="font-bold text-slate-200">FastAPI (Python)</span>
                    </div>
                </div>
                <p className="text-xs text-slate-500 mt-8">Version 1.0.0 • Project Showcase 2026</p>
            </GlassCard>
        </div>
    );
}
