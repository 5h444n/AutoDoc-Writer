import React from "react";
import { Outlet } from "react-router-dom";
import { TopBar } from "./TopBar";
import { Sidebar } from "./Sidebar";
import { useApp } from "../../context/AppContext";

export function AppLayout() {
  const { isOffline } = useApp();

  return (
    <div className="min-h-screen bg-background">
      <TopBar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 page-enter">
          {isOffline && (
            <div className="mb-4 p-3 rounded-lg bg-destructive/10 border border-destructive/20 flex items-center gap-2 text-sm text-destructive animate-slide-in-up">
              <span className="font-medium">Offline mode:</span>
              <span className="text-destructive/80">Showing cached documentation. Generation is unavailable.</span>
            </div>
          )}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
