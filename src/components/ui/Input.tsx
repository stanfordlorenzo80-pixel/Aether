import * as React from 'react';
import { cn } from '@/lib/utils';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  label?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, leftIcon, rightIcon, label, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="mb-1.5 block text-xs font-medium text-aether-text-secondary">
            {label}
          </label>
        )}
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-aether-text-tertiary">
              {leftIcon}
            </div>
          )}
          <input
            type={type}
            className={cn(
              'flex h-10 w-full rounded-lg border bg-aether-surface-0 px-3 py-2 text-sm text-aether-text-primary transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-aether-text-tertiary focus-visible:outline-none focus-visible:border-aether-border-focus focus-visible:ring-1 focus-visible:ring-aether-border-focus disabled:cursor-not-allowed disabled:opacity-50',
              error ? 'border-aether-error focus-visible:border-aether-error focus-visible:ring-aether-error/20' : 'border-aether-border hover:border-aether-border-active',
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              className
            )}
            ref={ref}
            {...props}
          />
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-aether-text-tertiary">
              {rightIcon}
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-xs text-aether-error animate-fade-in">{error}</p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };
