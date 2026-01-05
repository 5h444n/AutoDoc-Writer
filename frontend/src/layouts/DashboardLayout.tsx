import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/Sidebar";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#020617]"> {/* Extremely dark slate background */}
      
      {/* Sidebar Component */}
      <Sidebar />

      {/* Main Content Area */}
      {/* md:pl-64 pushes content to the right on desktop to make room for fixed sidebar */}
      <main className="transition-all duration-300 md:pl-64">
        
        {/* Header / Top Bar (Optional but adds polish) */}
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-white/5 bg-[#020617]/80 px-6 backdrop-blur-xl">
          <h2 className="text-sm font-medium text-slate-400">Dashboard / Overview</h2>
          {/* We can add a mobile menu toggle here later */}
        </header>

        {/* Dynamic Page Content */}
        <div className="p-6 md:p-8 animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  );
}