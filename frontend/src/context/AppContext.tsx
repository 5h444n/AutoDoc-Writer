import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

type FormatStyle = "plainText" | "research" | "latex";

type AppContextValue = {
  isOffline: boolean;
  setIsOffline: (offline: boolean) => void;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  defaultFormat: FormatStyle;
  setDefaultFormat: (format: FormatStyle) => void;
  textComplexity: number;
  setTextComplexity: (complexity: number) => void;
  notificationsEnabled: boolean;
  setNotificationsEnabled: (enabled: boolean) => void;
  cacheEnabled: boolean;
  setCacheEnabled: (enabled: boolean) => void;
};

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [isOffline, setIsOffline] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [defaultFormat, setDefaultFormat] = useState<FormatStyle>("plainText");
  const [textComplexity, setTextComplexity] = useState(50);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [cacheEnabled, setCacheEnabled] = useState(true);

  const toggleDarkMode = () => {
    setIsDarkMode((prev) => !prev);
  };

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const value = useMemo(
    () => ({
      isOffline,
      setIsOffline,
      isDarkMode,
      toggleDarkMode,
      defaultFormat,
      setDefaultFormat,
      textComplexity,
      setTextComplexity,
      notificationsEnabled,
      setNotificationsEnabled,
      cacheEnabled,
      setCacheEnabled,
    }),
    [
      isOffline,
      isDarkMode,
      defaultFormat,
      textComplexity,
      notificationsEnabled,
      cacheEnabled,
    ],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}
