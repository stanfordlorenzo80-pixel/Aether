import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { useUIStore } from '@/lib/store';
import type { EngineStatus } from '@/lib/types';

export function useAether() {
  const [connected, setConnected] = useState(false);
  const [latency, setLatency] = useState<number | undefined>(undefined);
  const [error, setError] = useState<string | undefined>(undefined);
  
  const setEngineStatus = useUIStore((state) => state.setEngineStatus);

  useEffect(() => {
    let mounted = true;
    let timeoutId: number;

    const checkHealth = async () => {
      try {
        const start = performance.now();
        const status = await api.health();
        const end = performance.now();
        
        if (!mounted) return;

        if (status.running) {
          setConnected(true);
          setLatency(end - start);
          setError(undefined);
          setEngineStatus(status);
        } else {
          setConnected(false);
          setLatency(undefined);
          setError('Engine is offline');
          setEngineStatus(status);
        }
      } catch (err) {
        if (!mounted) return;
        setConnected(false);
        setLatency(undefined);
        setError(err instanceof Error ? err.message : 'Failed to connect');
      }

      // Poll every 5 seconds
      if (mounted) {
        timeoutId = window.setTimeout(checkHealth, 5000);
      }
    };

    // Initial check
    checkHealth();

    return () => {
      mounted = false;
      window.clearTimeout(timeoutId);
    };
  }, [setEngineStatus]);

  return { connected, latency, error };
}
