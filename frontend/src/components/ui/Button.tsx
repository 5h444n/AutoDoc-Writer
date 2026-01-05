import React from "react";
import { Loader2 } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, children, isLoading, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={isLoading || disabled}
        className={cn(
          // Layout & Centering (FIXED HERE)
          "relative flex w-full items-center justify-center gap-2", 
          "text-center align-middle",
          
          // Sizing & Shape
          "rounded-xl py-3.5 px-8 text-sm font-semibold",
          
          // Visuals (Colors & Shadows)
          "text-white transition-all duration-300",
          "bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500",
          "shadow-[0_0_20px_rgba(99,102,241,0.5)] hover:shadow-[0_0_30px_rgba(99,102,241,0.7)]",
          
          // States
          "disabled:opacity-50 disabled:cursor-not-allowed",
          "active:scale-[0.98]",
          
          className
        )}
        {...props}
      >
        {isLoading && <Loader2 className="h-4 w-4 animate-spin text-white" />}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";