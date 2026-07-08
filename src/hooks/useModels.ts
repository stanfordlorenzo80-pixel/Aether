import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import { useModelStore } from '@/lib/store';
import { DEFAULT_PROVIDER, DEFAULT_MODEL } from '@/lib/constants';

export function useModels() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const providers = useModelStore((state) => state.providers);
  const activeModel = useModelStore((state) => state.activeModel);
  const setProviders = useModelStore((state) => state.setProviders);
  const setActiveModel = useModelStore((state) => state.setActiveModel);

  const fetchProviders = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.listProviders();
      setProviders(data);
      
      // If we have providers but no active model set, or the active model doesn't exist,
      // pick a sensible default
      if (data.length > 0) {
        let foundActive = false;
        for (const p of data) {
          if (p.models && p.models.some(m => m.id === activeModel)) {
            foundActive = true;
            break;
          }
        }
        
        if (!foundActive) {
          // Try to find a provider with models, prefer connected ones
          const connectedWithModels = data.find(p => p.status === 'connected' && p.models && p.models.length > 0);
          const anyWithModels = data.find(p => p.models && p.models.length > 0);
          const nextProvider = connectedWithModels || anyWithModels;
          
          if (nextProvider && nextProvider.models.length > 0) {
            // Try default model first, then first available
            const defaultModel = nextProvider.models.find(m => m.id === DEFAULT_MODEL);
            const nextModel = defaultModel || nextProvider.models[0];
            setActiveModel(nextProvider.id, nextModel.id);
          }
        }
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch models');
    } finally {
      setIsLoading(false);
    }
  }, [setProviders, activeModel, setActiveModel]);

  useEffect(() => {
    fetchProviders();
  }, [fetchProviders]);

  const testConnection = async (providerId: string) => {
    const result = await api.testConnection(providerId);
    // Refresh providers after testing to get updated status
    await fetchProviders();
    return result;
  };

  // Flatten models for dropdowns
  const allModels = providers.flatMap(p => 
    (p.models || []).map(m => ({ ...m, providerInfo: p }))
  );

  return {
    providers,
    models: allModels,
    activeModel,
    setActiveModel,
    refreshModels: fetchProviders,
    testConnection,
    isLoading,
    error
  };
}
