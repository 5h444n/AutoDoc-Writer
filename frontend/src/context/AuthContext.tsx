import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { fetchCurrentUser, loginWithGitHub } from "../lib/api";
import type { User } from "../lib/types";

type AuthContextValue = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: () => void;
  logout: () => void;
  setAuthToken: (token: string | null) => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("auth_token"));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    fetchCurrentUser()
      .then((profile) => setUser(profile))
      .catch(() => {
        localStorage.removeItem("auth_token");
        setToken(null);
        setUser(null);
      })
      .finally(() => setIsLoading(false));
  }, [token]);

  const login = useCallback(() => {
    setIsLoading(true);
    loginWithGitHub();
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("username");
    localStorage.removeItem("name");
    localStorage.removeItem("avatar");
    setToken(null);
    setUser(null);
  }, []);

  const setAuthToken = useCallback((newToken: string | null) => {
    if (newToken) {
      localStorage.setItem("auth_token", newToken);
    } else {
      localStorage.removeItem("auth_token");
    }
    setToken(newToken);
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
      setAuthToken,
    }),
    [user, isLoading, login, logout, setAuthToken],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
