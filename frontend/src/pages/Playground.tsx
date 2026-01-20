import { useState } from "react";
import { Button } from "../components/ui/Button";
import { Sparkles, FileCode, Check, AlertCircle } from "lucide-react";

export default function PlaygroundPage() {
  const [code, setCode] = useState("");
  const [style, setStyle] = useState("standard");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!code.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult("");

    try {
        const token = localStorage.getItem("auth_token");
        const response = await fetch("http://localhost:8000/api/v1/ai/preview", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ code, style })
        });

        if (!response.ok) {
            throw new Error("Failed to generate documentation");
        }

        const data = await response.json();
        setResult(data.documentation || data); // Adjust based on actual response structure
    } catch (err: any) {
        setError(err.message);
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
        {/* Header */}
        <div>
            <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
                <Sparkles className="h-8 w-8 text-indigo-400" />
                AI Playground
            </h1>
            <p className="mt-2 text-slate-400">
                Test the documentation engine. Paste a code snippet to see how the AI interprets it.
            </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[600px]">
            {/* Input Section */}
            <div className="flex flex-col space-y-4 h-full">
                <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                        <FileCode className="h-4 w-4" />
                        Source Code
                    </label>
                    <select 
                        value={style} 
                        onChange={(e) => setStyle(e.target.value)}
                        className="bg-white/5 border border-white/10 rounded-lg px-3 py-1 text-sm text-slate-300 focus:outline-none focus:border-indigo-500"
                    >
                        <option value="standard">Standard Style</option>
                        <option value="latex">Mathematical (LaTeX)</option>
                    </select>
                </div>
                
                <textarea 
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Paste your Python, JavaScript, or TypeScript function here..."
                    className="flex-1 w-full bg-[#0b1221] border border-white/10 rounded-xl p-4 font-mono text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 resize-none"
                    spellCheck={false}
                />

                <Button 
                    onClick={handleGenerate} 
                    isLoading={loading}
                    className="w-full bg-indigo-600 hover:bg-indigo-500"
                >
                    <Sparkles className="h-4 w-4 mr-2" />
                    Generate Documentation
                </Button>
            </div>

            {/* Output Section */}
            <div className="flex flex-col space-y-4 h-full">
                <div className="flex items-center justify-between h-[30px]">
                     <label className="text-sm font-medium text-slate-300">Generated Output</label>
                     {result && <span className="text-emerald-400 text-xs flex items-center"><Check className="h-3 w-3 mr-1" /> Generated successfully</span>}
                </div>

                <div className="flex-1 w-full bg-white/5 border border-white/10 rounded-xl p-6 overflow-auto relative group">
                    {error ? (
                        <div className="absolute inset-0 flex items-center justify-center text-red-400 bg-red-500/5">
                            <div className="text-center">
                                <AlertCircle className="h-8 w-8 mx-auto mb-2 opacity-50" />
                                <p>{error}</p>
                            </div>
                        </div>
                    ) : result ? (
                        <div className="prose prose-invert max-w-none">
                            <pre className="whitespace-pre-wrap font-sans text-slate-300 leading-relaxed">
                                {result}
                            </pre>
                        </div>
                    ) : (
                        <div className="absolute inset-0 flex items-center justify-center text-slate-600">
                             <div className="text-center">
                                <Sparkles className="h-10 w-10 mx-auto mb-3 opacity-20" />
                                <p>Documentation will appear here</p>
                             </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    </div>
  );
}
