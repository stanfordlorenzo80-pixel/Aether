import * as React from 'react';
import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

export function SettingsView() {
  const [isChecking, setIsChecking] = useState(false);
  const [updateStatus, setUpdateStatus] = useState<string | null>(null);

  const checkForUpdates = async () => {
    try {
      setIsChecking(true);
      setUpdateStatus('Checking for updates...');
      const update = await check();
      
      if (update) {
        setUpdateStatus(`Update ${update.version} found! Downloading...`);
        let downloaded = 0;
        let contentLength = 0;
        
        await update.downloadAndInstall((event) => {
          if (event.event === 'Started') {
            contentLength = event.data.contentLength || 0;
            setUpdateStatus(`Downloading ${update.version}...`);
          } else if (event.event === 'Progress') {
            downloaded += event.data.chunkLength;
            // setUpdateStatus(`Downloading: ${Math.round((downloaded / contentLength) * 100)}%`);
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
      setUpdateStatus(`Update failed: ${err.message}`);
    } finally {
      setIsChecking(false);
    }
  };

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
          <Card variant="elevated" className="border-t-4 border-t-aether-accent">
            <CardHeader>
              <CardTitle>Cloud Inference</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="Anthropic API Key (Claude)" 
                type="password" 
                placeholder="sk-ant-..." 
                defaultValue="sk-ant-mock-key-for-now"
              />
              <p className="text-xs text-aether-text-tertiary">Keys are securely encrypted in the local OS keychain.</p>
            </CardContent>
          </Card>

          <Card variant="elevated" className="border-t-4 border-t-aether-warning">
            <CardHeader>
              <CardTitle>Local Inference</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input 
                label="Ollama API URL" 
                type="text" 
                defaultValue="http://127.0.0.1:11434"
              />
              <div className="flex justify-between items-center mt-4">
                <p className="text-xs text-aether-text-tertiary">Aether will automatically scan both 127.0.0.1 and localhost.</p>
                <Button size="sm" variant="secondary">Test Connection</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
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
          
          <Card variant="glass">
            <CardHeader>
              <CardTitle>Engine Diagnostics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-aether-text-secondary">
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Backend Port:</span> <span>8420</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Execution Mode:</span> <span>Standalone Sidecar</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Memory Store:</span> <span>Local TF-Vector</span></div>
              <div className="flex justify-between"><span className="text-aether-text-tertiary">Version:</span> <span>v0.1.0-alpha</span></div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
