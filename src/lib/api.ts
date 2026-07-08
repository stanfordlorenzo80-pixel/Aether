import type { EngineStatus, ProviderInfo, ConnectionStatus } from './types';

export class AetherAPI {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async health(): Promise<EngineStatus> {
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      if (!res.ok) throw new Error('Engine not healthy');
      const data = await res.json();
      return {
        running: true,
        version: data.version,
        uptime: data.uptime,
        port: parseInt(new URL(this.baseUrl).port || '80', 10),
        providers: data.providers,
      };
    } catch (e) {
      return { running: false, version: '0.0.0', port: parseInt(new URL(this.baseUrl).port || '80', 10) };
    }
  }

  async listProviders(): Promise<ProviderInfo[]> {
    const res = await fetch(`${this.baseUrl}/api/models/providers`);
    if (!res.ok) throw new Error('Failed to fetch providers');
    return res.json();
  }

  async testConnection(providerId: string): Promise<ConnectionStatus> {
    const res = await fetch(`${this.baseUrl}/api/models/test/${providerId}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to test connection');
    return res.json();
  }

  async saveApiKey(provider: string, key: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/settings/api-key`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider, key }),
    });
    if (!res.ok) throw new Error('Failed to save API key');
    return res.json();
  }

  async setOllamaUrl(url: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/settings/ollama-url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    if (!res.ok) throw new Error('Failed to update Ollama URL');
    return res.json();
  }

  async refreshProvider(providerId: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/providers/refresh/${providerId}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to refresh provider');
    return res.json();
  }

  async refreshAllProviders(): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/providers/refresh`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to refresh providers');
    return res.json();
  }
}

export const api = new AetherAPI('http://localhost:8420');
