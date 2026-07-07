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
  
  // Streaming chat is handled separately via useStream hook using standard fetch/SSE
}

export const api = new AetherAPI('http://localhost:8420');
