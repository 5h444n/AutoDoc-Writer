import React from 'react';
import { cn } from '@/lib/utils';

interface SkeletonCardProps {
  className?: string;
  lines?: number;
}

export function SkeletonCard({ className, lines = 3 }: SkeletonCardProps) {
  return (
    <div className={cn('p-4 rounded-lg border border-border bg-card animate-fade-in', className)}>
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full shimmer" />
        <div className="flex-1 space-y-2">
          <div className="h-4 w-1/3 rounded shimmer" />
          <div className="h-3 w-1/4 rounded shimmer" />
        </div>
      </div>
      <div className="space-y-2">
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className="h-3 rounded shimmer"
            style={{ width: `${Math.random() * 40 + 60}%` }}
          />
        ))}
      </div>
    </div>
  );
}

export function SkeletonList({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
