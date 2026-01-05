import { Button } from "../components/ui/Button";
import { Plus, Github, Search } from "lucide-react";

export default function RepositoriesPage() {
  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Repositories</h1>
          <p className="mt-1 text-slate-400">Manage and track your documentation projects.</p>
        </div>
        <div className="shrink-0">
            <Button className="w-full sm:w-auto shadow-lg shadow-indigo-500/20">
                <Plus className="h-4 w-4 mr-2" />
                Add Repository
            </Button>
        </div>
      </div>

      {/* Filter / Search Bar for Content (Visual Only) */}
      <div className="flex items-center gap-4 border-y border-white/5 py-4">
        <div className="relative flex-1 max-w-sm">
           <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
           <input 
              placeholder="Filter repositories..." 
              className="w-full rounded-lg border border-white/10 bg-white/5 py-2 pl-9 pr-4 text-sm text-white focus:border-indigo-500/50 focus:outline-none"
           />
        </div>
      </div>

      {/* --- High-End Empty State --- */}
      <div className="flex min-h-[400px] flex-col items-center justify-center rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.02] to-transparent p-8 text-center animate-fade-in">
        
        {/* Animated Icon Container */}
        <div className="group relative mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/5 ring-1 ring-white/10 transition-all hover:scale-105 hover:bg-white/10 hover:shadow-2xl hover:shadow-indigo-500/20">
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <Github className="h-10 w-10 text-slate-400 group-hover:text-white transition-colors" />
        </div>

        <h3 className="text-xl font-semibold text-white">No repositories connected</h3>
        <p className="mt-2 max-w-md text-sm text-slate-400 leading-relaxed">
          You haven't connected any GitHub repositories yet. Connect a repository to let AutoDoc start generating your documentation automatically.
        </p>

        <div className="mt-8">
          <Button className="bg-white text-slate-900 hover:bg-slate-200 hover:text-slate-900 shadow-none border border-transparent">
             Connect your first repository
          </Button>
        </div>
      </div>
    </div>
  );
}