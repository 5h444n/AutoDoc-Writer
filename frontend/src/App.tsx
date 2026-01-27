import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import axios from 'axios'

import { motion } from "framer-motion";
import { Sparkles, Github } from "lucide-react";
import { GlassCard } from "./components/ui/GlassCard";
import { GlowButton } from "./components/ui/GlowButton";

// --- Components ---

function Login() {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/api/v1/auth/login'
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-[#030712] relative overflow-hidden selection:bg-blue-500/30">
      {/* Background Grid & Ambient Glow */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
      <div className="absolute top-[-20%] left-[20%] w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-[120px]" />
      <div className="absolute top-[-20%] right-[20%] w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[120px]" />

      {/* The Login Card */}
      <GlassCard className="max-w-md w-full text-center relative z-10 p-10 border-white/10 bg-slate-900/40">
        {/* Logo Animation */}
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mx-auto w-20 h-20 bg-gradient-to-tr from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center mb-8 shadow-[0_0_40px_rgba(37,99,235,0.4)]"
        >
          <Sparkles className="w-10 h-10 text-white" />
        </motion.div>

        {/* Title */}
        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">
          AutoDoc <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">Writer</span>
        </h1>
        <p className="text-slate-400 mb-8 text-lg">
          Intelligent documentation for intelligent code.
        </p>

        {/* The CRITICAL Action Button */}
        <div className="w-full">
          <GlowButton onClick={handleLogin} className="w-full justify-center text-lg py-4 group">
            <Github className="w-5 h-5 mr-2 group-hover:text-white transition-colors" />
            Continue with GitHub
          </GlowButton>
        </div>

        <p className="mt-8 text-xs text-slate-600 uppercase tracking-widest font-semibold">
          Powered by Gemini 2.0 Flash
        </p>
      </GlassCard>
    </div>
  )
}

import Dashboard from './pages/Dashboard'

function AuthHandler({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const checkAuth = async () => {
      // 1. Check URL for token
      const params = new URLSearchParams(location.search)
      const rawToken = params.get('access_token') || params.get('github_token')
      const tokenFromUrl = rawToken ? rawToken.replace(/^"|"$/g, '') : null

      if (tokenFromUrl) {
        // Save to localStorage
        localStorage.setItem('access_token', tokenFromUrl)
        localStorage.setItem('github_token', tokenFromUrl) // Also save as github_token for Dashboard compatibility

        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname)
      }

      // 2. Check localStorage
      const token = localStorage.getItem('access_token')

      if (token) {
        // Set default axios header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        setIsAuthenticated(true)
      } else {
        setIsAuthenticated(false)
      }

      setLoading(false)
    }

    checkAuth()
  }, [location])

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  return <>{children}</>
}

// Ensure protected routes only render if authenticated
function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('access_token')
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  return (
    <Router>
      <AuthHandler>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthHandler>
    </Router>
  )
}

export default App
