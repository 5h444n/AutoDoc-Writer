import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setAuthToken } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    const username = searchParams.get('username');

    if (token) {
      setAuthToken(token);
      if (username) {
        localStorage.setItem('username', username);
      }
      navigate('/dashboard', { replace: true });
    } else {
      navigate('/', { replace: true });
    }
  }, [navigate, searchParams, setAuthToken]);

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center text-foreground">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mb-4" />
      <p className="text-muted-foreground">Authenticating...</p>
    </div>
  );
}
