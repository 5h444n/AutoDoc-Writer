import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import DashboardLayout from "./layouts/DashboardLayout";
import RepositoriesPage from "./pages/Repositories";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LoginPage />} />
        
        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          {/* Index route renders when user hits /dashboard */}
          <Route index element={<RepositoriesPage />} />
          
          {/* Placeholder for settings */}
          <Route path="settings" element={<div className="text-white">Settings Page Coming Soon</div>} />
        </Route>

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;