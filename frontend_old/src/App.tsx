import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import AuthCallback from "./pages/AuthCallback";
import DashboardLayout from "./layouts/DashboardLayout";
import RepositoriesPage from "./pages/Repositories";
import PlaygroundPage from "./pages/Playground";
import SettingsPage from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        
        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          {/* Index route renders when user hits /dashboard */}
          <Route index element={<RepositoriesPage />} />
          <Route path="playground" element={<PlaygroundPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;