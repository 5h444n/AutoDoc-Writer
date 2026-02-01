import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AppContextType {
  isOffline: boolean;
  setIsOffline: (offline: boolean) => void;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  defaultFormat: 'plainText' | 'research' | 'latex';
  setDefaultFormat: (format: 'plainText' | 'research' | 'latex') => void;
  textComplexity: number;
  setTextComplexity: (complexity: number) => void;
  notificationsEnabled: boolean;
  setNotificationsEnabled: (enabled: boolean) => void;
  cacheEnabled: boolean;
  setCacheEnabled: (enabled: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [isOffline, setIsOffline] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [defaultFormat, setDefaultFormat] = useState<'plainText' | 'research' | 'latex'>('plainText');
  const [textComplexity, setTextComplexity] = useState(50);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [cacheEnabled, setCacheEnabled] = useState(true);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  // Initialize dark mode
  React.useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  return (
    <AppContext.Provider
      value={{
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
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
