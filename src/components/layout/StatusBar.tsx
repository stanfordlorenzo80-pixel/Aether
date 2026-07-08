import * as React from 'react';
import { cn } from '@/lib/utils';
import { APP_VERSION } from '@/lib/constants';
import { useModelStore } from '@/lib/store';

export interface StatusBarProps {
  connected: boolean;
  latency?: number;
}

export function StatusBar({ connected, latency }: StatusBarProps) {
  const activeModel = useModelStore(state => state.activeModel);

  return (
    <footer className="flex h-7 shrink-0 items-center justify-between px-3 border-t border-aether-border bg-aether-surface-0 text-[11px] text-aether-text-tertiary z-20 select-none">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <div className={cn("w-1.5 h-1.5 rounded-full", connected ? "bg-aether-success/70" : "bg-aether-error/70")} />
          <span>Engine: {connected ? 'Online' : 'Offline'}</span>
        </div>
        
        <div className="w-[1px] h-3 bg-aether-border" />
        
        <span>Model: {activeModel}</span>
      </div>

      <div className="flex items-center gap-3">
        {latency !== undefined && (
          <>
            <span>{latency.toFixed(0)}ms</span>
            <div className="w-[1px] h-3 bg-aether-border" />
          </>
        )}
        <span>v{APP_VERSION}</span>
      </div>
    </footer>
  );
}
