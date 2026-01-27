import { Activity, Code2, Clock, FileCheck } from 'lucide-react';

export function RepoStats({ repo }: { repo: any }) {
    if (!repo) return null;

    // Real Data Logic
    const sizeInKB = repo.size || 0;
    const complexity = sizeInKB < 5000 ? 'Low' : sizeInKB < 25000 ? 'Medium' : 'High';

    // Est. Time: Math.ceil(repo.size / 1000) + 5 seconds
    const estTimeSeconds = Math.ceil(sizeInKB / 1000) + 5;
    const time = `~${estTimeSeconds}s`;

    const health = (repo.open_issues_count || 0) > 15 ? 'Needs Love 🟠' : 'Stable 🟢';

    const color = repo.language === 'TypeScript' ? 'text-blue-600' :
        repo.language === 'Python' ? 'text-yellow-600' : 'text-gray-600';

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-[#111]/50 p-4 rounded-xl border border-white/5 shadow-sm hover:border-white/10 transition-colors">
                <div className="flex items-center gap-2 text-gray-500 mb-1">
                    <Code2 className="h-4 w-4" />
                    <span className="text-xs font-medium">Language</span>
                </div>
                <p className={`text-lg font-bold ${color}`}>{repo.language || 'Unknown'}</p>
            </div>

            <div className="bg-[#111]/50 p-4 rounded-xl border border-white/5 shadow-sm hover:border-white/10 transition-colors">
                <div className="flex items-center gap-2 text-gray-500 mb-1">
                    <Activity className="h-4 w-4" />
                    <span className="text-xs font-medium">Complexity</span>
                </div>
                <p className="text-lg font-bold text-gray-200">{complexity}</p>
            </div>

            <div className="bg-[#111]/50 p-4 rounded-xl border border-white/5 shadow-sm hover:border-white/10 transition-colors">
                <div className="flex items-center gap-2 text-gray-500 mb-1">
                    <Clock className="h-4 w-4" />
                    <span className="text-xs font-medium">Est. Time</span>
                </div>
                <p className="text-lg font-bold text-gray-200">{time}</p>
            </div>

            <div className="bg-[#111]/50 p-4 rounded-xl border border-white/5 shadow-sm hover:border-white/10 transition-colors">
                <div className="flex items-center gap-2 text-gray-500 mb-1">
                    <FileCheck className="h-4 w-4" />
                    <span className="text-xs font-medium">Health</span>
                </div>
                <p className={`text-lg font-bold ${health.includes('Stable') ? 'text-green-400' : 'text-orange-400'}`}>
                    {health}
                </p>
            </div>
        </div>
    );
}
