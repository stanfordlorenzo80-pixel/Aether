import * as React from 'react';
import { cn } from '@/lib/utils';
import { Select } from '@/components/ui/Select';
import { motion } from 'framer-motion';
import { useModels } from '@/lib/hooks';

export interface HeaderProps {
  title: string;
  connected: boolean;
}

export function Header({ title, connected }: HeaderProps) {
  const { models, activeModel, setActiveModel } = useModels();

  // Build options from real model data
  const modelOptions = models.map(m => ({
    value: m.id,
    label: `${m.name}${m.providerInfo?.type === 'local' ? ' (Local)' : ''}`,
  }));

  // Fallback if no models loaded yet
  if (modelOptions.length === 0) {
    modelOptions.push({ value: 'loading', label: 'Loading models...' });
  }

  const handleModelChange = (value: string) => {
    const selectedModel = models.find(m => m.id === value);
    if (selectedModel) {
      setActiveModel(selectedModel.provider, selectedModel.id);
    }
  };

  return (
    <header className="flex h-14 shrink-0 items-center justify-between px-6 border-b border-aether-border bg-transparent z-10">
      <div className="flex items-center gap-4">
        <motion.h1 
          key={title}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-lg font-semibold tracking-tight text-aether-text-primary"
        >
          {title}
        </motion.h1>
      </div>

      <div className="flex items-center gap-4">
        <div className="w-56">
          <Select 
            value={activeModel || modelOptions[0]?.value} 
            onChange={handleModelChange} 
            options={modelOptions} 
            className="h-8 py-1 bg-transparent border-aether-border hover:bg-aether-surface-1"
          />
        </div>
        
        <div className="flex items-center gap-2" title={connected ? "Engine Connected" : "Engine Disconnected"}>
          <div className="relative flex h-2.5 w-2.5">
            {connected && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-aether-success opacity-40"></span>
            )}
            <span className={cn(
              "relative inline-flex rounded-full h-2.5 w-2.5",
              connected ? "bg-aether-success" : "bg-aether-error"
            )}></span>
          </div>
        </div>
      </div>
    </header>
  );
}
