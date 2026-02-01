import * as React from "react";
import { cn } from "../../lib/utils";

type SliderProps = Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange" | "value"> & {
  value?: number[];
  onValueChange?: (value: number[]) => void;
};

export function Slider({ value = [0], onValueChange, className, ...props }: SliderProps) {
  const currentValue = value[0] ?? 0;
  return (
    <div className={cn("flex items-center", className)}>
      <input
        type="range"
        className="w-full"
        value={currentValue}
        onChange={(event) => onValueChange?.([Number(event.target.value)])}
        {...props}
      />
    </div>
  );
}
