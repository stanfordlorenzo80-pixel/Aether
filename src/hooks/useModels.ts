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
          if (p.models.some(m => m.id === activeModel)) {
            foundActive = true;
            break;
          }
        }
        
        if (!foundActive) {
          // Try to find the default model, otherwise pick the first available
          let nextProvider = data.find(p => p.id === DEFAULT_PROVIDER) || data[0];
          let nextModel = nextProvider.models.find(m => m.id === DEFAULT_MODEL) || nextProvider.models[0];
          
          if (nextProvider && nextModel) {
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
    return api.testConnection(providerId);
  };

  // Flatten models for dropdowns
  const allModels = providers.flatMap(p => 
    p.models.map(m => ({ ...m, providerInfo: p }))
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
