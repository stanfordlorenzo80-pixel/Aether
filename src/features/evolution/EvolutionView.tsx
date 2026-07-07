import * as React from 'react';

export function EvolutionView() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <div className="w-16 h-16 rounded-xl bg-aether-surface-2 border border-aether-border flex items-center justify-center mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-aether-text-secondary"><path d="m2 22 5-5"/><path d="m17 7 5-5"/><path d="M10 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M14 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M10 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M14 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/></svg>
      </div>
      <h2 className="text-xl font-semibold text-aether-text-primary mb-2">System Evolution</h2>
      <p className="text-aether-text-secondary max-w-md">
        Recursive self-improvement loops and Phi metric evaluation. Coming in Phase 4.
      </p>
    </div>
  );
}
