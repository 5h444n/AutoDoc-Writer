import * as React from "react";

import { cn } from "../../lib/utils";

type DropdownContextValue = {
  open: boolean;
  setOpen: (open: boolean) => void;
};

const DropdownContext = React.createContext<DropdownContextValue | undefined>(undefined);

function useDropdownContext() {
  const context = React.useContext(DropdownContext);
  if (!context) {
    throw new Error("DropdownMenu components must be used within DropdownMenu");
  }
  return context;
}

type DropdownMenuProps = {
  children: React.ReactNode;
};

function DropdownMenu({ children }: DropdownMenuProps) {
  const [open, setOpen] = React.useState(false);

  return (
    <DropdownContext.Provider value={{ open, setOpen }}>
      <div className="relative inline-flex">{children}</div>
    </DropdownContext.Provider>
  );
}

type DropdownMenuTriggerProps = {
  asChild?: boolean;
  children: React.ReactElement;
};

function DropdownMenuTrigger({ asChild, children }: DropdownMenuTriggerProps) {
  const { open, setOpen } = useDropdownContext();
  const toggle = (event: React.MouseEvent) => {
    children.props.onClick?.(event);
    setOpen(!open);
  };

  if (asChild) {
    return React.cloneElement(children, {
      onClick: toggle,
    });
  }

  return (
    <button type="button" onClick={toggle}>
      {children}
    </button>
  );
}

type DropdownMenuContentProps = React.HTMLAttributes<HTMLDivElement> & {
  align?: "start" | "end";
};

function DropdownMenuContent({ className, align = "start", ...props }: DropdownMenuContentProps) {
  const { open } = useDropdownContext();
  if (!open) {
    return null;
  }

  return (
    <div
      className={cn(
        "absolute z-50 mt-2 min-w-[10rem] rounded-md border border-border bg-popover p-1 text-popover-foreground shadow-md",
        align === "end" ? "right-0" : "left-0",
        className,
      )}
      {...props}
    />
  );
}

type DropdownMenuItemProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

function DropdownMenuItem({ className, onClick, ...props }: DropdownMenuItemProps) {
  const { setOpen } = useDropdownContext();
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onClick?.(event);
    setOpen(false);
  };

  return (
    <button
      type="button"
      className={cn(
        "flex w-full cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors hover:bg-accent hover:text-accent-foreground",
        className,
      )}
      onClick={handleClick}
      {...props}
    />
  );
}

type DropdownMenuLabelProps = React.HTMLAttributes<HTMLDivElement>;

function DropdownMenuLabel({ className, ...props }: DropdownMenuLabelProps) {
  return (
    <div className={cn("px-2 py-1.5 text-sm font-semibold", className)} {...props} />
  );
}

function DropdownMenuSeparator() {
  return <div className="my-1 h-px bg-border" />;
}

export {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
};
