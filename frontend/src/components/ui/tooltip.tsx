import * as React from "react";
import { cn } from "../../lib/utils";

type TooltipContextValue = {
  open: boolean;
  setOpen: (open: boolean) => void;
};

const TooltipContext = React.createContext<TooltipContextValue | undefined>(undefined);

function useTooltipContext() {
  const context = React.useContext(TooltipContext);
  if (!context) {
    throw new Error("Tooltip components must be used within Tooltip");
  }
  return context;
}

function Tooltip({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(false);
  return (
    <TooltipContext.Provider value={{ open, setOpen }}>
      <span className="relative inline-flex">{children}</span>
    </TooltipContext.Provider>
  );
}

function TooltipTrigger({ asChild, children }: { asChild?: boolean; children: React.ReactElement }) {
  const { setOpen } = useTooltipContext();
  const triggerProps = {
    onMouseEnter: (event: React.MouseEvent) => {
      children.props.onMouseEnter?.(event);
      setOpen(true);
    },
    onMouseLeave: (event: React.MouseEvent) => {
      children.props.onMouseLeave?.(event);
      setOpen(false);
    },
  };
  if (asChild) {
    return React.cloneElement(children, triggerProps);
  }
  return (
    <span {...triggerProps}>
      {children}
    </span>
  );
}

function TooltipContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const { open } = useTooltipContext();
  if (!open) return null;
  return (
    <div
      className={cn(
        "absolute z-50 mt-2 rounded-md border border-border bg-popover px-2 py-1 text-xs text-popover-foreground shadow-md",
        className,
      )}
      {...props}
    />
  );
}

export { Tooltip, TooltipContent, TooltipTrigger };
