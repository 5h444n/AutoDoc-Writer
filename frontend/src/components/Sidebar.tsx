import { LayoutDashboard, Settings, LogOut, Bot, Sparkles, ChevronRight } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function Sidebar() {
  const location = useLocation();

  const navItems = [
    { icon: LayoutDashboard, label: "Repositories", href: "/dashboard" },
    { icon: Settings, label: "Settings", href: "/dashboard/settings" },
  ];

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-white/5 bg-[#0b1221]/95 backdrop-blur-xl transition-transform max-md:-translate-x-full">
      {/* --- Branding --- */}
      <div className="flex h-16 items-center px-6 border-b border-white/5">
        <div className="flex items-center gap-3 font-bold text-white">
          <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 shadow-lg shadow-indigo-500/20">
            <Bot className="h-5 w-5 text-white" />
            <div className="absolute -right-1 -top-1 rounded-full bg-[#0b1221] p-0.5">
              <Sparkles className="h-2.5 w-2.5 text-amber-300 fill-amber-300" />
            </div>
          </div>
          <span className="text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            AutoDoc
          </span>
        </div>
      </div>

      {/* --- Navigation --- */}
      <nav className="flex-1 space-y-1 px-3 py-6">
        <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-2">Platform</p>
        {navItems.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                "group relative flex items-center rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-300",
                isActive
                  ? "bg-white/5 text-white"
                  : "text-slate-400 hover:bg-white/5 hover:text-white"
              )}
            >
              {/* Active Glowing Indicator */}
              {isActive && (
                <div className="absolute left-0 h-6 w-1 rounded-r-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.6)]" />
              )}
              
              <item.icon
                className={cn(
                  "mr-3 h-5 w-5 transition-colors",
                  isActive ? "text-indigo-400" : "text-slate-500 group-hover:text-slate-300"
                )}
              />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* --- User Profile --- */}
      <div className="p-4 border-t border-white/5">
        <button className="group flex w-full items-center gap-3 rounded-xl bg-gradient-to-b from-white/5 to-transparent p-3 border border-white/5 transition-all hover:border-white/10 hover:shadow-lg">
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 p-[1px]">
            <div className="h-full w-full rounded-full bg-[#0b1221] flex items-center justify-center">
               <span className="text-xs font-bold text-white">EL</span>
            </div>
          </div>
          <div className="flex-1 text-left">
            <p className="truncate text-sm font-medium text-white group-hover:text-indigo-300 transition-colors">Engineering Lead</p>
            <p className="truncate text-xs text-slate-500">Free Plan</p>
          </div>
          <LogOut className="h-4 w-4 text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity" />
        </button>
      </div>
    </aside>
  );
}