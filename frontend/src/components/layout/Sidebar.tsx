import React from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  GitBranch,
  GitCommit,
  FileText,
  Download,
  Settings,
  HelpCircle,
} from "lucide-react";
import { cn } from "../../lib/utils";

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
  { icon: GitBranch, label: 'Repositories', path: '/repositories' },
  { icon: GitCommit, label: 'Commits', path: '/commits' },
  { icon: FileText, label: 'Documentation', path: '/documentation' },
  { icon: Download, label: 'Export', path: '/export' },
];

const bottomNavItems = [
  { icon: Settings, label: 'Settings', path: '/settings' },
  { icon: HelpCircle, label: 'Help & About', path: '/help' },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-56 bg-sidebar border-r border-sidebar-border flex flex-col h-[calc(100vh-3.5rem)] sticky top-14">
      <nav className="flex-1 py-4 px-3 space-y-1">
        {navItems.map((item, index) => {
          const isActive = location.pathname === item.path;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group relative overflow-hidden',
                isActive
                  ? 'bg-sidebar-accent text-sidebar-primary'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground'
              )}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {isActive && (
                <span className="absolute left-0 top-0 bottom-0 w-0.5 bg-sidebar-primary animate-slide-in-left" />
              )}
              <item.icon
                className={cn(
                  'h-5 w-5 transition-transform duration-200 group-hover:scale-110',
                  isActive && 'text-sidebar-primary'
                )}
              />
              <span>{item.label}</span>
              {isActive && (
                <span className="absolute right-2 w-1.5 h-1.5 rounded-full bg-sidebar-primary pulse-dot" />
              )}
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-sidebar-border py-4 px-3 space-y-1">
        {bottomNavItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group relative',
                isActive
                  ? 'bg-sidebar-accent text-sidebar-primary'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent/50'
              )}
            >
              {isActive && (
                <span className="absolute left-0 top-0 bottom-0 w-0.5 bg-sidebar-primary animate-slide-in-left" />
              )}
              <item.icon className="h-5 w-5 transition-transform duration-200 group-hover:scale-110" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
}
