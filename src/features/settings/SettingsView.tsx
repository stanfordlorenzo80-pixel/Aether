import * as React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';

export function SettingsView() {
  return (
    <div className="p-8 max-w-3xl mx-auto h-full overflow-y-auto scrollbar-thin">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-aether-text-primary">Settings</h2>
        <p className="text-aether-text-secondary mt-1">Configure Aether preferences and API keys.</p>
      </div>

      <div className="space-y-6">
        <Card variant="elevated">
          <CardHeader>
            <CardTitle>API Keys</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input 
              label="Anthropic API Key (Claude)" 
              type="password" 
              placeholder="sk-ant-..." 
              defaultValue="sk-ant-mock-key-for-now"
            />
            <p className="text-xs text-aether-text-tertiary">Keys are stored securely in your local system keychain.</p>
          </CardContent>
        </Card>

        <Card variant="elevated">
          <CardHeader>
            <CardTitle>Local Inference (Ollama)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input 
              label="Ollama API URL" 
              type="text" 
              defaultValue="http://localhost:11434"
            />
            <div className="flex justify-end mt-2">
              <Button size="sm" variant="secondary">Test Connection</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
