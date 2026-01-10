import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button'; 
import { Github, ArrowRight } from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!username) return alert("Please enter GitHub username!");
    navigate('/converter');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleLogin();
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-[#0f172a] overflow-hidden">
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px]"></div>
      <div className="relative z-10 w-full max-w-[420px] px-6">
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 p-10 rounded-[3rem] text-center shadow-2xl">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <Github className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white mb-8">AutoDoc <span className="text-indigo-400">Writer</span></h1>
          <input 
            type="text" 
            placeholder="Enter GitHub Username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
            className="w-full p-5 bg-white/5 border border-white/10 rounded-2xl outline-none focus:ring-2 focus:ring-indigo-400 text-white text-center mb-5"
          />
          <Button onClick={handleLogin} className="w-full py-6 bg-white text-indigo-950 rounded-2xl font-bold flex justify-center group">
            Continue <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Login;