import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button'; 
import { Github, LayoutDashboard,  LogOut,  FileCode } from 'lucide-react';

const BACKEND_URL = "http://localhost:8000"; // আপনার টিমেটের পোর্ট অনুযায়ী এটি চেক করুন

const Converter = () => {
  const [inputCode, setInputCode] = useState('');
  const [latexOutput, setLatexOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleConvert = async () => {
    if (!inputCode) return alert("Select code first!");
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/convert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: inputCode }),
      });
      const data = await response.json();
      setLatexOutput(data.latex);
    } catch (_e) { alert("Backend Connection Error!"); }
    finally { setIsLoading(false); }
  };

  return (
    <div className="flex h-screen bg-[#0d1117] text-[#c9d1d9]">
      {/* Sidebar */}
      <div className="w-16 border-r border-[#30363d] flex flex-col items-center py-6 gap-8 bg-[#161b22]">
        <Github size={28} />
        <LayoutDashboard size={20} className="text-white" />
        <LogOut size={20} className="mt-auto cursor-pointer" onClick={() => navigate('/')} />
      </div>

      {/* Repository Dashboard Area */}
      <div className="w-72 border-r border-[#30363d] p-4 flex flex-col">
        <h2 className="text-sm font-bold mb-4">Repositories</h2>
        <div className="space-y-2 overflow-y-auto">
          <div className="p-2 hover:bg-[#161b22] rounded cursor-pointer border-b border-white/5">
            <span className="text-[#58a6ff] text-sm font-semibold hover:underline">my-cool-project</span>
            <div className="flex items-center gap-2 mt-1 text-[10px] text-gray-500"><FileCode size={12}/> main.py</div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        <header className="h-14 border-b border-[#30363d] flex items-center justify-between px-6">
          <span className="text-xs font-bold text-gray-400">LATEX WORKSPACE</span>
          <Button onClick={handleConvert} disabled={isLoading} className="bg-[#238636] hover:bg-[#2ea043] text-xs h-8 px-4 font-bold">
            {isLoading ? "Converting..." : "Convert to LaTeX"}
          </Button>
        </header>
        <div className="flex-1 flex overflow-hidden">
          <textarea 
            className="flex-1 bg-transparent p-6 outline-none font-mono text-sm border-r border-[#30363d]"
            placeholder="Paste your code here..."
            value={inputCode}
            onChange={(e) => setInputCode(e.target.value)}
          />
          <div className="flex-1 p-6 bg-[#010409] font-mono text-sm text-indigo-300 overflow-auto leading-relaxed">
            {latexOutput || "LaTeX Preview will appear here..."}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Converter;