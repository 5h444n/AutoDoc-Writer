import { useEffect, useState } from "react";
import { Button } from "../components/ui/Button";
import { Plus, Github, Search, GitFork, Calendar, ExternalLink, Power } from "lucide-react";

interface Repository {
  name: string;
  url: string;
  last_updated: string;
  is_active: boolean;
}

export default function RepositoriesPage() {
  const [repos, setRepos] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Toggle Function
  const handleToggle = async (repoName: string, currentStatus: boolean) => {
    try {
        const token = localStorage.getItem("auth_token");
        // Optimistic Update
        setRepos(repos.map(r => r.name === repoName ? { ...r, is_active: !currentStatus } : r));

        const response = await fetch(`http://localhost:8000/api/v1/repos/${repoName}/toggle`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ is_active: !currentStatus })
        });

        if (!response.ok) {
            throw new Error("Failed to update status");
        }
    } catch (err) {
        // Revert on failure
        setRepos(repos.map(r => r.name === repoName ? { ...r, is_active: currentStatus } : r));
        console.error("Toggle failed", err);
    }
  };

  useEffect(() => {
    const fetchRepos = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        if (!token) {
          setError("No authentication token found");
          setLoading(false);
          return;
        }

        const response = await fetch("http://localhost:8000/api/v1/repos/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error("Unauthorized - Please login again");
            }
            throw new Error("Failed to fetch repositories");
        }

        const data = await response.json();
        setRepos(data.repos || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchRepos();
  }, []);

  if (loading) {
     return (
        <div className="flex h-[50vh] items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
     );
  }

  if (error) {
      return (
         <div className="p-8 text-center border border-red-500/20 bg-red-500/10 rounded-2xl">
             <h3 className="text-red-400 text-lg font-medium">Error Loading Repositories</h3>
             <p className="text-red-300 mt-2">{error}</p>
             <Button className="mt-4" onClick={() => window.location.reload()}>Retry</Button>
         </div>
      )
  }

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

      {/* Filter / Search Bar for Content */}
      <div className="flex items-center gap-4 border-y border-white/5 py-4">
        <div className="relative flex-1 max-w-sm">
           <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
           <input 
              placeholder="Filter repositories..." 
              className="w-full rounded-lg border border-white/10 bg-white/5 py-2 pl-9 pr-4 text-sm text-white focus:border-indigo-500/50 focus:outline-none"
           />
        </div>
      </div>

      {/* Content Area */}
      {repos.length === 0 ? (
          /* --- High-End Empty State --- */
          <div className="flex min-h-[400px] flex-col items-center justify-center rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.02] to-transparent p-8 text-center animate-fade-in">
            <div className="group relative mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/5 ring-1 ring-white/10 transition-all hover:scale-105 hover:bg-white/10 hover:shadow-2xl hover:shadow-indigo-500/20">
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <Github className="h-10 w-10 text-slate-400 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-semibold text-white">No repositories connected</h3>
            <p className="mt-2 text-sm text-slate-400 leading-relaxed max-w-md">
              You haven't connected any GitHub repositories yet. Connect a repository to let AutoDoc start generating your documentation automatically.
            </p>
            <div className="mt-8">
              <Button className="bg-white text-slate-900 hover:bg-slate-200 hover:text-slate-900 shadow-none border border-transparent">
                 Connect your first repository
              </Button>
            </div>
          </div>
      ) : (
          /* --- Repo List --- */
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 animate-fade-in">
            {repos.map((repo) => (
              <div 
                 key={repo.name}
                 className="group relative rounded-2xl border border-white/10 bg-white/[0.02] p-6 hover:bg-white/[0.04] transition-all hover:shadow-xl hover:shadow-indigo-500/5 flex flex-col h-full"
              >
                  <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                             <Github className="h-5 w-5 text-indigo-400" />
                          </div>
                          <div className="overflow-hidden">
                              <h3 className="text-lg font-semibold text-white group-hover:text-indigo-400 transition-colors truncate" title={repo.name}>{repo.name}</h3>
                              <p className="text-xs text-slate-400 flex items-center gap-1">
                                  GitHub
                              </p>
                          </div>
                      </div>
                      <a 
                        href={repo.url} 
                        target="_blank" 
                        rel="noreferrer"
                        className="text-slate-500 hover:text-white transition-colors"
                      >
                          <ExternalLink className="h-4 w-4" />
                      </a>
                  </div>

                  <div className="space-y-3 flex-1">
                       <div className="flex items-center text-sm text-slate-400">
                           <GitFork className="h-4 w-4 mr-2 text-slate-600" />
                           <span>Branch: main</span>
                       </div>
                        <div className="flex items-center text-sm text-slate-400">
                           <Calendar className="h-4 w-4 mr-2 text-slate-600" />
                           <span>Updated: {new Date(repo.last_updated).toLocaleDateString()}</span>
                       </div>
                  </div>
                  
                  <div className="mt-6 pt-6 border-t border-white/5 flex items-center justify-between">
                     <span className={`px-2.5 py-1 rounded-full text-xs font-medium border flex items-center gap-1.5 transition-colors ${
                         repo.is_active 
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                            : 'bg-slate-500/10 text-slate-400 border-slate-500/20'
                     }`}>
                         <span className={`w-1.5 h-1.5 rounded-full ${ repo.is_active ? 'bg-emerald-400' : 'bg-slate-400'}`}></span>
                         {repo.is_active ? 'Monitored' : 'Inactive'}
                     </span>

                     <button 
                        onClick={() => handleToggle(repo.name, repo.is_active)}
                        className={`
                            h-8 w-8 rounded-lg flex items-center justify-center transition-all
                            ${repo.is_active 
                                ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20' 
                                : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20'
                            }
                        `}
                        title={repo.is_active ? "Stop Monitoring" : "Start Monitoring"}
                     >
                        <Power className="h-4 w-4" />
                     </button>
                  </div>
              </div>
            ))}
          </div>
      )}
    </div>
  );
}