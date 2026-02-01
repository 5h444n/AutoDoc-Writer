import React from "react";
import { cn } from "../../lib/utils";

type Status = "active" | "inactive" | "pending" | "success" | "error";

type StatusBadgeProps = {
  status: Status;
  label?: string;
  showDot?: boolean;
  className?: string;
};

const statusStyles: Record<Status, string> = {
  active: "bg-accent/10 text-accent border-accent/20",
  inactive: "bg-muted text-muted-foreground border-border",
  pending: "bg-primary/10 text-primary border-primary/20",
  success: "bg-accent/10 text-accent border-accent/20",
  error: "bg-destructive/10 text-destructive border-destructive/20",
};

const dotStyles: Record<Status, string> = {
  active: "bg-accent",
  inactive: "bg-muted-foreground",
  pending: "bg-primary",
  success: "bg-accent",
  error: "bg-destructive",
};

export function StatusBadge({ status, label, showDot = true, className }: StatusBadgeProps) {
  const defaultLabels: Record<Status, string> = {
    active: "Active",
    inactive: "Inactive",
    pending: "Pending",
    success: "Success",
    error: "Error",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-all duration-200",
        statusStyles[status],
        className,
      )}
    >
      {showDot && (
        <span
          className={cn(
            "w-1.5 h-1.5 rounded-full",
            dotStyles[status],
            status === "active" && "pulse-dot",
            status === "pending" && "animate-pulse-soft",
          )}
        />
      )}
      {label || defaultLabels[status]}
    </span>
  );
}
