import * as React from "react";
import { cn } from "../../lib/utils";

type TabsContextValue = {
  value: string;
  setValue: (value: string) => void;
};

const TabsContext = React.createContext<TabsContextValue | undefined>(undefined);

function useTabsContext() {
  const context = React.useContext(TabsContext);
  if (!context) {
    throw new Error("Tabs components must be used within Tabs");
  }
  return context;
}

type TabsProps = {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
};

function Tabs({ value, defaultValue, onValueChange, children }: TabsProps) {
  const [internal, setInternal] = React.useState(defaultValue ?? "");
  const currentValue = value ?? internal;
  const setValue = (next: string) => {
    if (value === undefined) {
      setInternal(next);
    }
    onValueChange?.(next);
  };

  return (
    <TabsContext.Provider value={{ value: currentValue, setValue }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
}

const TabsList = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("inline-flex items-center gap-1", className)} {...props} />
  ),
);
TabsList.displayName = "TabsList";

type TabsTriggerProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  value: string;
};

const TabsTrigger = React.forwardRef<HTMLButtonElement, TabsTriggerProps>(
  ({ className, value, ...props }, ref) => {
    const { value: activeValue, setValue } = useTabsContext();
    const isActive = activeValue === value;
    return (
      <button
        ref={ref}
        type="button"
        data-state={isActive ? "active" : "inactive"}
        className={cn(
          "px-3 py-1.5 text-sm font-medium rounded-md transition-colors",
          isActive ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground",
          className,
        )}
        onClick={() => setValue(value)}
        {...props}
      />
    );
  },
);
TabsTrigger.displayName = "TabsTrigger";

type TabsContentProps = React.HTMLAttributes<HTMLDivElement> & {
  value: string;
};

const TabsContent = React.forwardRef<HTMLDivElement, TabsContentProps>(
  ({ className, value, ...props }, ref) => {
    const { value: activeValue } = useTabsContext();
    if (activeValue !== value) {
      return null;
    }
    return <div ref={ref} className={cn("mt-2", className)} {...props} />;
  },
);
TabsContent.displayName = "TabsContent";

export { Tabs, TabsList, TabsTrigger, TabsContent };
