import { useState } from "react";
import { Button } from "../components/ui/Button";
import { Github, Bot, Sparkles } from "lucide-react";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-[#0f172a] overflow-hidden">
      
      {/* --- Dynamic Background Animation --- */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div
          className="absolute top-0 right-1/4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"
          style={{ animationDelay: "2s" }}
        ></div>
        <div
          className="absolute -bottom-32 left-1/3 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"
          style={{ animationDelay: "4s" }}
        ></div>
      </div>

      {/* --- Glassmorphism Card --- */}
      <div className="relative z-10 w-full max-w-[420px] mx-4 animate-fade-in">
        <div className="relative group rounded-2xl bg-gradient-to-b from-white/10 to-white/5 p-[1px] shadow-2xl backdrop-blur-xl">
          
          <div className="bg-[#0f172a]/80 backdrop-blur-xl rounded-2xl p-8 sm:p-10 border border-white/10">
            
            {/* BRANDING SECTION */}
            <div className="flex flex-col items-center mb-10">
              {/* Logo Icon Container */}
              <div className="relative h-16 w-16 bg-gradient-to-tr from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg mb-6 group-hover:scale-105 transition-transform duration-300">
                {/* Replaced 'AD' with a Bot Icon */}
                <Bot className="h-8 w-8 text-white" />
                
                {/* Tiny sparkle accent */}
                <div className="absolute -top-2 -right-2 bg-white rounded-full p-1 shadow-md">
                   <Sparkles className="h-3 w-3 text-purple-600" />
                </div>
              </div>
              
              {/* Full Name */}
              <h1 className="text-3xl font-bold text-white tracking-tight mb-2">
                AutoDoc Writer
              </h1>
              <p className="text-slate-400 text-sm text-center max-w-[260px]">
                Intelligent documentation generation for your engineering team.
              </p>
            </div>

            {/* ACTION SECTION */}
            <div className="space-y-6">
              <Button onClick={handleLogin} isLoading={isLoading}>
                {!isLoading && <Github className="h-5 w-5" />}
                <span>Continue with GitHub</span>
              </Button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-white/10" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-[#0f172a] px-2 text-slate-500">
                    Secure Access
                  </span>
                </div>
              </div>
            </div>
            
            {/* FOOTER */}
            <p className="mt-8 text-center text-xs text-slate-500">
              By clicking continue, you agree to our{" "}
              <a href="#" className="text-indigo-400 hover:text-indigo-300 transition-colors hover:underline">Terms</a>
              {" "}and{" "}
              <a href="#" className="text-indigo-400 hover:text-indigo-300 transition-colors hover:underline">Privacy Policy</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}