import * as React from "react";
import { cn } from "../../lib/utils";

type SelectContextValue = {
  value?: string;
  setValue: (value: string) => void;
  open: boolean;
  setOpen: (open: boolean) => void;
};

const SelectContext = React.createContext<SelectContextValue | undefined>(undefined);

function useSelectContext() {
  const context = React.useContext(SelectContext);
  if (!context) {
    throw new Error("Select components must be used within Select");
  }
  return context;
}

type SelectProps = {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
};

function Select({ value, defaultValue, onValueChange, children }: SelectProps) {
  const [internalValue, setInternalValue] = React.useState(defaultValue);
  const [open, setOpen] = React.useState(false);
  const currentValue = value ?? internalValue;

  const setValue = (next: string) => {
    if (value === undefined) {
      setInternalValue(next);
    }
    onValueChange?.(next);
    setOpen(false);
  };

  return (
    <SelectContext.Provider value={{ value: currentValue, setValue, open, setOpen }}>
      <div className="relative inline-flex">{children}</div>
    </SelectContext.Provider>
  );
}

const SelectTrigger = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, ...props }, ref) => {
    const { open, setOpen } = useSelectContext();
    return (
      <button
        ref={ref}
        type="button"
        className={cn(
          "flex h-10 items-center justify-between rounded-md border border-border bg-background px-3 py-2 text-sm",
          className,
        )}
        onClick={() => setOpen(!open)}
        {...props}
      />
    );
  },
);
SelectTrigger.displayName = "SelectTrigger";

function SelectValue({ placeholder }: { placeholder?: string }) {
  const { value } = useSelectContext();
  return <span>{value ?? placeholder}</span>;
}

const SelectContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    const { open } = useSelectContext();
    if (!open) return null;
    return (
      <div
        ref={ref}
        className={cn(
          "absolute z-50 mt-1 w-full rounded-md border border-border bg-popover p-1 shadow-md",
          className,
        )}
        {...props}
      />
    );
  },
);
SelectContent.displayName = "SelectContent";

type SelectItemProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  value: string;
};

const SelectItem = React.forwardRef<HTMLButtonElement, SelectItemProps>(
  ({ className, value, ...props }, ref) => {
    const { value: activeValue, setValue } = useSelectContext();
    const isActive = activeValue === value;
    return (
      <button
        ref={ref}
        type="button"
        className={cn(
          "flex w-full cursor-pointer items-center rounded-sm px-2 py-1.5 text-sm text-foreground hover:bg-accent hover:text-accent-foreground",
          isActive && "bg-accent text-accent-foreground",
          className,
        )}
        onClick={() => setValue(value)}
        {...props}
      />
    );
  },
);
SelectItem.displayName = "SelectItem";

export { Select, SelectContent, SelectItem, SelectTrigger, SelectValue };
