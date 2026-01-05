import { useState } from "react";
import { Button } from "../components/ui/Button";

// GitHub SVG Icon (Inline for zero-dependency)
const GitHubIcon = () => (
  <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
  </svg>
);

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = () => {
    setIsLoading(true);
    // Simulate network delay to demonstrate UI state
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-50 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl border border-gray-100 animate-in fade-in zoom-in duration-500">
        
        {/* Branding Header */}
        <div className="text-center mb-10">
          <div className="h-12 w-12 bg-slate-900 rounded-xl mx-auto flex items-center justify-center mb-4 shadow-lg shadow-slate-900/20 group cursor-default">
            <span className="text-white font-bold text-xl group-hover:scale-110 transition-transform">AD</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 mb-2">
            Welcome back
          </h1>
          <p className="text-sm text-slate-500 px-8">
            Sign in to AutoDoc Writer to generate documentation for your repositories.
          </p>
        </div>

        {/* Login Actions */}
        <div className="space-y-6">
          <Button 
            onClick={handleLogin} 
            isLoading={isLoading} 
            className="w-full h-12 text-base shadow-sm"
          >
            {!isLoading && <GitHubIcon />}
            Continue with GitHub
          </Button>
          
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-gray-200" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-slate-400 font-medium">
                Secure Authentication
              </span>
            </div>
          </div>
        </div>

        {/* Legal Footer */}
        <p className="mt-8 text-center text-xs text-slate-400">
          By continuing, you agree to our{" "}
          <a href="#" className="underline decoration-slate-300 underline-offset-4 hover:text-slate-900 hover:decoration-slate-900 transition-all">Terms</a>{" "}
          and{" "}
          <a href="#" className="underline decoration-slate-300 underline-offset-4 hover:text-slate-900 hover:decoration-slate-900 transition-all">Privacy Policy</a>.
        </p>
      </div>
    </div>
  );
}