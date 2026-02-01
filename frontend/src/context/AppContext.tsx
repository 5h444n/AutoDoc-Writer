import React, { createContext, useContext, useMemo, useState } from "react";

type AppContextValue = {
  isOffline: boolean;
  setIsOffline: (offline: boolean) => void;
};

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [isOffline, setIsOffline] = useState(false);

  const value = useMemo(
    () => ({
      isOffline,
      setIsOffline,
    }),
    [isOffline],
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
