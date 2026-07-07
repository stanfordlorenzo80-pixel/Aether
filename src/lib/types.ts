export type ViewId = 'playground' | 'cortex' | 'evolution' | 'models' | 'settings';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  model?: string;
  tokens?: number;
  latency?: number;
  isStreaming?: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  model: string;
  createdAt: number;
  updatedAt: number;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  contextWindow: number;
  description?: string;
  capabilities?: string[];
}

export interface ProviderInfo {
  id: string;
  name: string;
  type: 'cloud' | 'local';
  status: 'connected' | 'disconnected' | 'error';
  models: ModelInfo[];
  icon?: string;
}

export interface ConnectionStatus {
  connected: boolean;
  latency?: number;
  error?: string;
}

export interface EngineStatus {
  running: boolean;
  version: string;
  uptime?: number;
  port: number;
  providers?: string[];
}

export interface StreamChunk {
  type: 'content' | 'error' | 'done' | 'metadata';
  content?: string;
  error?: string;
  metadata?: Record<string, any>;
}

export interface AppSettings {
  apiKeys: Record<string, string>;
  defaultModel: string;
  defaultProvider: string;
  theme: 'dark' | 'light';
  enginePort: number;
  ollamaUrl: string;
}
