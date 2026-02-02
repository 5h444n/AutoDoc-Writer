import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { AppProvider } from "@/context/AppContext";
import { AppLayout } from "@/components/layout/AppLayout";
import Welcome from "./pages/Welcome";
import AuthCallback from "./pages/AuthCallback";
import Dashboard from "./pages/Dashboard";
import Repositories from "./pages/Repositories";
import Commits from "./pages/Commits";
import Documentation from "./pages/Documentation";
import Export from "./pages/Export";
import Settings from "./pages/Settings";
import Help from "./pages/Help";
import NotFound from "./pages/NotFound";
import LoginPage from "./pages/Login";
import DashboardLayout from "./layouts/DashboardLayout";
import RepositoriesPage from "./pages/Repositories";
import PlaygroundPage from "./pages/Playground";
import SettingsPage from "./pages/Settings";

const queryClient = new QueryClient();

// Protected route wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
}

// Auth redirect wrapper
function AuthRedirect({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary" />
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public route - Welcome/Login */}
      <Route
        path="/"
        element={
          <AuthRedirect>
            <Welcome />
          </AuthRedirect>
        }
      />
      <Route path="/login" element={<LoginPage />} />

      <Route path="/auth/callback" element={<AuthCallback />} />
      
      {/* Protected routes with app layout */}
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/repositories" element={<Repositories />} />
        <Route path="/commits" element={<Commits />} />
        <Route path="/documentation" element={<Documentation />} />
        <Route path="/export" element={<Export />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/help" element={<Help />} />
      </Route>
      
      {/* Protected Dashboard Routes */}
      <Route path="/dashboard" element={<DashboardLayout />}>
        {/* Index route renders when user hits /dashboard */}
        <Route index element={<RepositoriesPage />} />
        <Route path="playground" element={<PlaygroundPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      
      {/* Catch-all */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <AuthProvider>
        <AppProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
        </AppProvider>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
