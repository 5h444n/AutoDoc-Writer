import { LayoutDashboard, Settings, LogOut, Bot, Sparkles } from "lucide-react";
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
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-white/10 bg-[#0f172a] transition-transform max-md:-translate-x-full">
      {/* --- Logo Section --- */}
      <div className="flex h-16 items-center border-b border-white/10 px-6">
        <div className="flex items-center gap-2 font-bold text-white">
          <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500">
            <Bot className="h-5 w-5 text-white" />
            <div className="absolute -right-1 -top-1 rounded-full bg-white p-0.5">
              <Sparkles className="h-2 w-2 text-purple-600" />
            </div>
          </div>
          <span className="text-lg tracking-tight">AutoDoc</span>
        </div>
      </div>

      {/* --- Navigation --- */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                "group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-indigo-500/10 text-indigo-400 ring-1 ring-indigo-500/20"
                  : "text-slate-400 hover:bg-white/5 hover:text-white"
              )}
            >
              <item.icon
                className={cn(
                  "mr-3 h-5 w-5 flex-shrink-0 transition-colors",
                  isActive ? "text-indigo-400" : "text-slate-500 group-hover:text-white"
                )}
              />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* --- User Profile (Bottom) --- */}
      <div className="border-t border-white/10 p-4">
        <div className="flex items-center gap-3 rounded-xl bg-white/5 p-3 transition-colors hover:bg-white/10">
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-slate-700 to-slate-600 ring-2 ring-white/10" />
          <div className="flex-1 overflow-hidden">
            <p className="truncate text-sm font-medium text-white">Engineering Lead</p>
            <p className="truncate text-xs text-slate-400">user@company.com</p>
          </div>
          <button className="text-slate-400 hover:text-white">
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </div>
    </aside>
  );
}