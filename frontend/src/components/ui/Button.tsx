import React from "react";
import { Loader2 } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
  variant?: "primary" | "outline" | "ghost";
  size?: "default" | "sm" | "icon";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      children,
      isLoading,
      disabled,
      variant = "primary",
      size = "default",
      ...props
    },
    ref
  ) => {
    // Variant Styles
    const variants = {
      primary:
        "bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 shadow-lg shadow-indigo-500/25 border border-transparent text-white",
      outline:
        "bg-transparent border border-white/10 hover:bg-white/5 text-slate-300",
      ghost:
        "bg-transparent hover:bg-white/5 text-slate-400 hover:text-white",
    };

    // Size Styles
    const sizes = {
      default: "py-3.5 px-8 text-sm",
      sm: "py-2 px-4 text-xs",
      icon: "h-9 w-9 p-0",
    };

    return (
      <button
        ref={ref}
        disabled={isLoading || disabled}
        className={cn(
          // Layout & Centering
          "relative flex items-center justify-center gap-2",
          size === "icon" ? "rounded-full" : "w-full rounded-xl",
          "text-center align-middle font-semibold transition-all duration-300",
          "disabled:opacity-50 disabled:cursor-not-allowed",

          variants[variant],
          sizes[size],

          className
        )}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
