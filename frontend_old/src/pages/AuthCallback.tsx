import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");
    const username = searchParams.get("username");

    if (token) {
      localStorage.setItem("auth_token", token);
      if (username) {
        localStorage.setItem("username", username);
      }
      // Give a small delay or immediate redirect
      navigate("/dashboard", { replace: true });
    } else {
      // Failed login or missing params
      navigate("/", { replace: true });
    }
  }, [searchParams, navigate]);

  return (
    <div className="min-h-screen bg-[#0f172a] flex flex-col items-center justify-center text-white">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mb-4"></div>
      <p className="text-slate-400">Authenticating...</p>
    </div>
  );
}
