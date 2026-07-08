import * as React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useModels } from '@/lib/hooks';

export function ModelsView() {
  const { providers, models, activeModel, setActiveModel, testConnection, refreshModels, isLoading } = useModels();

  return (
    <div className="p-8 max-w-5xl mx-auto h-full overflow-y-auto scrollbar-thin">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-semibold text-aether-text-primary">Models & Providers</h2>
          <p className="text-aether-text-secondary mt-1">Manage cloud and local LLM connections.</p>
        </div>
        <Button onClick={refreshModels} loading={isLoading} variant="secondary">
          Refresh List
        </Button>
      </div>

      {/* Provider Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {providers.map((provider) => (
          <Card key={provider.id} variant="elevated">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
              <div>
                <CardTitle className="text-lg">{provider.name}</CardTitle>
                <CardDescription>{provider.type === 'cloud' ? 'Cloud Provider' : 'Local Inference'}</CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-aether-text-tertiary mr-1">
                  {provider.status === 'connected' ? 'Connected' : provider.status === 'error' ? 'Error' : 'Disconnected'}
                </span>
                <div className={`w-2.5 h-2.5 rounded-full ${
                  provider.status === 'connected' ? 'bg-aether-success' : 
                  provider.status === 'error' ? 'bg-aether-error' : 'bg-aether-text-tertiary'
                }`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mt-2">
                <span className="text-sm text-aether-text-secondary">
                  {(provider.models?.length || 0)} model{(provider.models?.length || 0) !== 1 ? 's' : ''} available
                </span>
                <Button size="sm" variant="secondary" onClick={() => testConnection(provider.id)}>Test Connection</Button>
              </div>
            </CardContent>
          </Card>
        ))}

        {providers.length === 0 && (
          <div className="col-span-3 text-center py-12">
            <p className="text-aether-text-tertiary">No providers registered. The engine may still be starting up.</p>
            <Button onClick={refreshModels} variant="secondary" className="mt-4">Retry</Button>
          </div>
        )}
      </div>

      {/* Models Table */}
      <h3 className="text-xl font-semibold text-aether-text-primary mb-4">
        Available Models
        <span className="text-sm font-normal text-aether-text-tertiary ml-2">({models.length} total)</span>
      </h3>

      {models.length > 0 ? (
        <div className="border border-aether-border rounded-xl overflow-hidden bg-aether-surface-1">
          <table className="w-full text-left text-sm">
            <thead className="bg-aether-surface-2 border-b border-aether-border text-aether-text-secondary">
              <tr>
                <th className="px-6 py-3 font-medium">Model Name</th>
                <th className="px-6 py-3 font-medium">Provider</th>
                <th className="px-6 py-3 font-medium">Context Window</th>
                <th className="px-6 py-3 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-aether-border">
              {models.map((model) => (
                <tr 
                  key={`${model.provider}-${model.id}`} 
                  className={`transition-colors hover:bg-aether-surface-2/50 ${activeModel === model.id ? 'bg-aether-accent-subtle/30' : ''}`}
                >
                  <td className="px-6 py-4">
                    <div className="font-medium text-aether-text-primary flex items-center gap-2">
                      {model.name}
                      {activeModel === model.id && (
                        <span className="px-2 py-0.5 rounded text-[10px] bg-aether-accent/20 text-aether-accent">Active</span>
                      )}
                    </div>
                    <div className="text-xs text-aether-text-tertiary mt-1">{model.id}</div>
                  </td>
                  <td className="px-6 py-4 text-aether-text-secondary">
                    <div className="flex items-center gap-2">
                      <div className={`w-1.5 h-1.5 rounded-full ${
                        model.providerInfo?.status === 'connected' ? 'bg-aether-success' : 'bg-aether-text-tertiary'
                      }`} />
                      {model.providerInfo?.name || model.provider}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-aether-text-secondary">{(model.contextWindow || 0).toLocaleString()} tokens</td>
                  <td className="px-6 py-4 text-right">
                    <Button 
                      size="sm" 
                      variant={activeModel === model.id ? 'ghost' : 'secondary'}
                      disabled={activeModel === model.id}
                      onClick={() => setActiveModel(model.provider, model.id)}
                    >
                      {activeModel === model.id ? 'Selected' : 'Select'}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="border border-aether-border rounded-xl bg-aether-surface-1 p-12 text-center">
          <p className="text-aether-text-secondary mb-2">No models detected yet.</p>
          <p className="text-sm text-aether-text-tertiary mb-4">
            Make sure Ollama is running locally, or add your API keys in Settings.
          </p>
          <Button onClick={refreshModels} variant="secondary">Refresh Models</Button>
        </div>
      )}
    </div>
  );
}
