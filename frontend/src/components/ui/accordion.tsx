import * as React from "react";
import { cn } from "../../lib/utils";

type AccordionContextValue = {
  openItem: string | null;
  setOpenItem: (value: string | null) => void;
  collapsible: boolean;
};

const AccordionContext = React.createContext<AccordionContextValue | undefined>(undefined);

const AccordionItemContext = React.createContext<string | null>(null);

function useAccordionContext() {
  const context = React.useContext(AccordionContext);
  if (!context) {
    throw new Error("Accordion components must be used within Accordion");
  }
  return context;
}

type AccordionProps = {
  type?: "single";
  collapsible?: boolean;
  children: React.ReactNode;
  className?: string;
};

function Accordion({ collapsible = true, children, className }: AccordionProps) {
  const [openItem, setOpenItem] = React.useState<string | null>(null);

  return (
    <AccordionContext.Provider value={{ openItem, setOpenItem, collapsible }}>
      <div className={className}>{children}</div>
    </AccordionContext.Provider>
  );
}

type AccordionItemProps = React.HTMLAttributes<HTMLDivElement> & {
  value: string;
};

function AccordionItem({ value, className, ...props }: AccordionItemProps) {
  return (
    <AccordionItemContext.Provider value={value}>
      <div className={cn("border-b border-border", className)} data-value={value} {...props} />
    </AccordionItemContext.Provider>
  );
}

type AccordionTriggerProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

function AccordionTrigger({ className, children, ...props }: AccordionTriggerProps) {
  const { openItem, setOpenItem, collapsible } = useAccordionContext();
  const itemValue = React.useContext(AccordionItemContext);
  if (!itemValue) {
    throw new Error("AccordionTrigger must be used within AccordionItem");
  }
  const isOpen = openItem === itemValue;
  const toggle = () => {
    if (isOpen && collapsible) {
      setOpenItem(null);
    } else {
      setOpenItem(itemValue);
    }
  };
  return (
    <button
      type="button"
      className={cn("flex w-full items-center justify-between py-3 text-sm font-medium", className)}
      onClick={toggle}
      {...props}
    >
      {children}
    </button>
  );
}

type AccordionContentProps = React.HTMLAttributes<HTMLDivElement>;

function AccordionContent({ className, ...props }: AccordionContentProps) {
  const { openItem } = useAccordionContext();
  const itemValue = React.useContext(AccordionItemContext);
  if (!itemValue || openItem !== itemValue) return null;
  return <div className={cn("pb-3 text-sm", className)} {...props} />;
}

export { Accordion, AccordionContent, AccordionItem, AccordionTrigger };
