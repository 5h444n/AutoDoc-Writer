import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/Sidebar";
import { Search, Bell } from "lucide-react";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 selection:bg-indigo-500/30">
      <Sidebar />

      <main className="transition-all duration-300 md:pl-64">
        {/* --- Top Header with Search & Actions --- */}
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-white/5 bg-[#020617]/80 px-6 backdrop-blur-xl">
          
          {/* Breadcrumb / Title */}
          <div className="flex items-center gap-4">
             <span className="text-sm font-medium text-slate-400">Dashboard</span>
             <span className="text-slate-600">/</span>
             <span className="text-sm font-medium text-white">Overview</span>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            {/* Search Input Placeholder */}
            <div className="hidden md:flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 focus-within:border-indigo-500/50 focus-within:bg-white/10 transition-all">
              <Search className="h-4 w-4 text-slate-500" />
              <input 
                type="text" 
                placeholder="Search..." 
                className="w-48 bg-transparent text-sm text-white placeholder-slate-500 focus:outline-none"
              />
            </div>

            {/* Notification Bell */}
            <button className="relative rounded-full p-2 text-slate-400 hover:bg-white/5 hover:text-white transition-colors">
              <Bell className="h-5 w-5" />
              <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-500 ring-2 ring-[#020617]" />
            </button>
          </div>
        </header>

        {/* --- Main Content with Ambient Background --- */}
        <div className="relative p-6 md:p-10">
          {/* Subtle purple glow in top right corner */}
          <div className="pointer-events-none absolute -top-20 right-0 h-96 w-96 rounded-full bg-indigo-500/10 blur-3xl" />
          
          <div className="relative animate-fade-in">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
}