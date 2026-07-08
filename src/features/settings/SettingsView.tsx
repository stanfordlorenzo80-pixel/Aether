import * as React from 'react';
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { api } from '@/lib/api';
import { useModels } from '@/lib/hooks';

// Tauri plugin imports — these are optional and only work inside the Tauri app context
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

export function SettingsView() {
  const { providers, refreshModels } = useModels();
  
  const [isChecking, setIsChecking] = useState(false);
  const [updateStatus, setUpdateStatus] = useState<string | null>(null);

  // API Key states
  const [claudeKey, setClaudeKey] = useState('');
  const [openrouterKey, setOpenrouterKey] = useState('');
  const [ollamaUrl, setOllamaUrl] = useState('http://127.0.0.1:11434');

  // Status states
  const [claudeStatus, setClaudeStatus] = useState<string | null>(null);
  const [openrouterStatus, setOpenrouterStatus] = useState<string | null>(null);
  const [ollamaStatus, setOllamaStatus] = useState<string | null>(null);
  const [savingClaude, setSavingClaude] = useState(false);
  const [savingOpenrouter, setSavingOpenrouter] = useState(false);
  const [savingOllama, setSavingOllama] = useState(false);

  // System Prompt states
  const [systemPrompt, setSystemPrompt] = useState('');
  const [savingPrompt, setSavingPrompt] = useState(false);
  const [promptStatus, setPromptStatus] = useState<string | null>(null);

  // Storage & Sync states
  const [obsidianPath, setObsidianPath] = useState('');
  const [webhookUrl, setWebhookUrl] = useState('');
  const [savingSync, setSavingSync] = useState(false);
  const [syncStatus, setSyncStatus] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8420/api/settings/system-prompt')
      .then(res => res.json())
      .then(data => { if (data.content) setSystemPrompt(data.content); })
      .catch(() => {});
      
    fetch('http://localhost:8420/api/settings/memory-sync')
      .then(res => res.json())
      .then(data => {
        if (data.obsidian_path) setObsidianPath(data.obsidian_path);
        if (data.webhook_url) setWebhookUrl(data.webhook_url);
      })
      .catch(() => {});
  }, []);

  // Populate live status from providers
  useEffect(() => {
    const claude = providers.find(p => p.id === 'claude');
    const openrouter = providers.find(p => p.id === 'openrouter');
    const ollama = providers.find(p => p.id === 'ollama');
    
    if (claude) setClaudeStatus(claude.status);
    if (openrouter) setOpenrouterStatus(openrouter.status);
    if (ollama) setOllamaStatus(ollama.status);
  }, [providers]);

  const handleSaveClaudeKey = async () => {
    setSavingClaude(true);
    setClaudeStatus(null);
    try {
      const result = await api.saveApiKey('claude', claudeKey);
      setClaudeStatus(result.success ? 'connected' : 'error');
      await refreshModels();
    } catch (err: any) {
      setClaudeStatus('error');
    } finally {
      setSavingClaude(false);
    }
  };

  const handleSaveOpenrouterKey = async () => {
    setSavingOpenrouter(true);
    setOpenrouterStatus(null);
    try {
      const result = await api.saveApiKey('openrouter', openrouterKey);
      setOpenrouterStatus(result.success ? 'connected' : 'error');
      await refreshModels();
    } catch (err: any) {
      setOpenrouterStatus('error');
    } finally {
      setSavingOpenrouter(false);
    }
  };

  const handleSaveOllamaUrl = async () => {
    setSavingOllama(true);
    setOllamaStatus(null);
    try {
      const result = await api.setOllamaUrl(ollamaUrl);
      setOllamaStatus(result.success ? 'connected' : 'error');
      await refreshModels();
    } catch (err: any) {
      setOllamaStatus('error');
    } finally {
      setSavingOllama(false);
    }
  };

  const handleSavePrompt = async () => {
    setSavingPrompt(true);
    setPromptStatus(null);
    try {
      const res = await fetch('http://localhost:8420/api/settings/system-prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: systemPrompt })
      });
      setPromptStatus(res.ok ? 'connected' : 'error');
    } catch {
      setPromptStatus('error');
    } finally {
      setSavingPrompt(false);
    }
  };

  const handleSaveSync = async () => {
    setSavingSync(true);
    setSyncStatus(null);
    try {
      const res = await fetch('http://localhost:8420/api/settings/memory-sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ obsidian_path: obsidianPath, webhook_url: webhookUrl })
      });
      setSyncStatus(res.ok ? 'connected' : 'error');
    } catch {
      setSyncStatus('error');
    } finally {
      setSavingSync(false);
    }
  };

  const handleTestConnection = async (providerId: string) => {
    try {
      const result = await api.testConnection(providerId);
      if (providerId === 'claude') setClaudeStatus(result.connected ? 'connected' : 'error');
      if (providerId === 'openrouter') setOpenrouterStatus(result.connected ? 'connected' : 'error');
      if (providerId === 'ollama') setOllamaStatus(result.connected ? 'connected' : 'error');
      await refreshModels();
    } catch (err) {
      // status already set
    }
  };

  const checkForUpdates = async () => {
    try {
      setIsChecking(true);
      setUpdateStatus('Checking for updates...');
      const update = await check();
      
      if (update) {
        setUpdateStatus(`Update ${update.version} found! Downloading...`);
        await update.downloadAndInstall((event: any) => {
          if (event.event === 'Started') {
            setUpdateStatus(`Downloading ${update.version}...`);
          } else if (event.event === 'Finished') {
            setUpdateStatus('Installing update...');
          }
        });

        setUpdateStatus('Update installed! Restarting...');
        await relaunch();
      } else {
        setUpdateStatus('Aether is up to date.');
      }
    } catch (err: any) {
      console.error(err);
      if (err.message && err.message.includes('undefined')) {
        setUpdateStatus('No update server configured.');
      } else {
        setUpdateStatus(`Update failed: ${err.message || 'No update server configured.'}`);
      }
    } finally {
      setIsChecking(false);
    }
  };

  const StatusDot = ({ status }: { status: string | null }) => (
    <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${
      status === 'connected' ? 'bg-aether-success' :
      status === 'error' ? 'bg-aether-error' :
      'bg-aether-text-tertiary'
    }`} />
  );

  return (
    <div className="p-8 max-w-4xl mx-auto h-full overflow-y-auto scrollbar-thin">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold text-aether-text-primary tracking-tight">System Configuration</h2>
          <p className="text-aether-text-secondary mt-2">Manage providers, update the engine, and configure Swarm peers.</p>
        </div>
        <div className="flex flex-col items-end">
          <Button 
            variant="primary" 
            onClick={checkForUpdates} 
            loading={isChecking}
            className="mb-2"
          >
            Check for Updates
          </Button>
          {updateStatus && <p className="text-xs text-aether-accent-secondary animate-fade-in">{updateStatus}</p>}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          {/* Claude */}
          <Card variant="elevated" className="border-t-4 border-t-aether-accent">
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>Anthropic Claude</CardTitle>
              <StatusDot status={claudeStatus} />
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="API Key" 
                type="password" 
                placeholder="sk-ant-..." 
                value={claudeKey}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setClaudeKey(e.target.value)}
              />
              <div className="flex justify-between items-center">
                <p className="text-xs text-aether-text-tertiary">
                  {claudeStatus === 'connected' ? '✓ Connected' : claudeStatus === 'error' ? '✗ Invalid key or network error' : 'Enter your Anthropic API key'}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" variant="secondary" onClick={() => handleTestConnection('claude')}>Test</Button>
                  <Button size="sm" variant="primary" onClick={handleSaveClaudeKey} loading={savingClaude}>Save Key</Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* OpenRouter */}
          <Card variant="elevated" className="border-t-4 border-t-purple-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>OpenRouter</CardTitle>
              <StatusDot status={openrouterStatus} />
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="API Key" 
                type="password" 
                placeholder="sk-or-..." 
                value={openrouterKey}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setOpenrouterKey(e.target.value)}
              />
              <div className="flex justify-between items-center">
                <p className="text-xs text-aether-text-tertiary">
                  {openrouterStatus === 'connected' ? '✓ Connected — access 100+ models' : openrouterStatus === 'error' ? '✗ Invalid key' : 'Unlock Llama, Mixtral, Command R+ and more'}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" variant="secondary" onClick={() => handleTestConnection('openrouter')}>Test</Button>
                  <Button size="sm" variant="primary" onClick={handleSaveOpenrouterKey} loading={savingOpenrouter}>Save Key</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          {/* Ollama */}
          <Card variant="elevated" className="border-t-4 border-t-aether-warning">
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>Ollama (Local)</CardTitle>
              <StatusDot status={ollamaStatus} />
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="Ollama API URL" 
                type="text" 
                value={ollamaUrl}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setOllamaUrl(e.target.value)}
              />
              <div className="flex justify-between items-center">
                <p className="text-xs text-aether-text-tertiary">
                  {ollamaStatus === 'connected' 
                    ? `✓ Connected — ${providers.find(p => p.id === 'ollama')?.models?.length || 0} models detected`
                    : 'Make sure Ollama is running locally'}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" variant="secondary" onClick={() => handleTestConnection('ollama')}>Test</Button>
                  <Button size="sm" variant="primary" onClick={handleSaveOllamaUrl} loading={savingOllama}>Save URL</Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Swarm */}
          <Card variant="elevated" className="border-t-4 border-t-aether-success">
            <CardHeader>
              <CardTitle>P2P Swarm Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="Swarm Peer Endpoint" 
                type="text" 
                placeholder="ws://192.168.1.100:8420/api/swarm/connect" 
              />
              <div className="flex justify-between items-center mt-4">
                <p className="text-xs text-aether-text-tertiary">Connect to peer nodes to distribute Cortex reasoning tasks.</p>
                <Button size="sm" variant="ghost" className="text-aether-success hover:bg-aether-success/10">Add Peer</Button>
              </div>
            </CardContent>
          </Card>

          {/* Cognitive Core */}
          <Card variant="elevated" className="border-t-4 border-t-aether-accent-secondary">
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>Cognitive Core (Safe Mode)</CardTitle>
              <StatusDot status={promptStatus} />
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-aether-text-secondary">Custom System Prompt</label>
                <textarea 
                  className="w-full h-32 px-3 py-2 bg-aether-surface-0 border border-aether-border rounded-md text-sm text-aether-text-primary focus:outline-none focus:border-aether-accent-secondary resize-none"
                  placeholder="Enter custom instructions to inject before all LLM prompts..."
                  value={systemPrompt}
                  onChange={(e) => setSystemPrompt(e.target.value)}
                />
              </div>
              <div className="flex justify-between items-center">
                <p className="text-xs text-aether-text-tertiary">
                  {promptStatus === 'connected' ? '✓ Saved successfully' : 'Overrides default behavior for all models'}
                </p>
                <Button size="sm" variant="primary" onClick={handleSavePrompt} loading={savingPrompt}>Save Prompt</Button>
              </div>
            </CardContent>
          </Card>

          {/* Storage & Memory Sync */}
          <Card variant="elevated">
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>Storage & Memory Sync</CardTitle>
              <StatusDot status={syncStatus} />
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-aether-text-secondary">Obsidian Vault Path (Absolute)</label>
                <input 
                  type="text" 
                  className="w-full px-3 py-2 bg-aether-surface-0 border border-aether-border rounded-md text-sm text-aether-text-primary focus:outline-none focus:border-aether-accent-secondary"
                  placeholder="e.g., C:\Users\LO\Documents\ObsidianVault\Aether_Brain"
                  value={obsidianPath}
                  onChange={(e) => setObsidianPath(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-aether-text-secondary">Web Sync (Webhook URL)</label>
                <input 
                  type="text" 
                  className="w-full px-3 py-2 bg-aether-surface-0 border border-aether-border rounded-md text-sm text-aether-text-primary focus:outline-none focus:border-aether-accent-secondary"
                  placeholder="e.g., https://hook.eu1.make.com/..."
                  value={webhookUrl}
                  onChange={(e) => setWebhookUrl(e.target.value)}
                />
              </div>
              <div className="flex justify-between items-center mt-4">
                <p className="text-xs text-aether-text-tertiary">
                  {syncStatus === 'connected' ? '✓ Settings saved successfully' : 'Sync memories as native markdown files'}
                </p>
                <Button size="sm" variant="primary" onClick={handleSaveSync} loading={savingSync}>Save Sync Settings</Button>
              </div>
            </CardContent>
          </Card>
          
          {/* Diagnostics */}
          <Card variant="glass">
            <CardHeader>
              <CardTitle>Engine Diagnostics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-aether-text-secondary">
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Backend Port:</span> <span>8420</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Execution Mode:</span> <span>Standalone Sidecar</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Memory Store:</span> <span>Local TF-Vector</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Providers:</span> <span>{providers.length} registered</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Total Models:</span> <span>{providers.reduce((sum, p) => sum + (p.models?.length || 0), 0)}</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Version:</span> <span>v0.1.0-alpha</span></div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
