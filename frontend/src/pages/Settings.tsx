import { Button } from "../components/ui/Button";
import { LogOut, Github, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function SettingsPage() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "Unknown User";

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("username");
    navigate("/");
  };

  return (
    <div className="space-y-8 max-w-3xl">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Settings</h1>
        <p className="mt-1 text-slate-400">Manage your account and preferences.</p>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl p-8 space-y-8">
          
          {/* Profile Section */}
          <div className="flex items-start justify-between">
              <div className="flex items-center space-x-4">
                  <div className="h-16 w-16 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white text-2xl font-bold">
                      {username.charAt(0).toUpperCase()}
                  </div>
                  <div>
                      <h3 className="text-xl font-semibold text-white">{username}</h3>
                      <p className="text-slate-400 text-sm flex items-center gap-1 mt-1">
                          <Github className="h-3 w-3" /> GitHub Account
                      </p>
                  </div>
              </div>
              <div className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-emerald-400 text-xs font-medium flex items-center gap-1">
                  <Shield className="h-3 w-3" /> Authenticated
              </div>
          </div>

          <div className="border-t border-white/5 pt-8">
              <h4 className="text-white font-medium mb-4">Account Actions</h4>
              <p className="text-slate-400 text-sm mb-6 max-w-lg">
                  Disconnecting your account will end your current session. You will need to re-authenticate with GitHub to access your repositories again.
              </p>
              
              <Button 
                variant="outline" 
                onClick={handleLogout}
                className="border-red-500/20 text-red-400 hover:bg-red-500/10 hover:border-red-500/30"
              >
                  <LogOut className="h-4 w-4 mr-2" />
                  Divconnect & Logout
              </Button>
          </div>
      </div>
      
      <div className="text-xs text-slate-500 text-center pt-8">
          AutoDoc Writer v1.0.0 • Built with React & FastAPI
      </div>
    </div>
  );
}
