import type { AppSettings } from './types';

export const ENGINE_PORT = 8420;
export const ENGINE_URL = `http://localhost:${ENGINE_PORT}`;
export const ENGINE_WS_URL = `ws://localhost:${ENGINE_PORT}`;

export const APP_VERSION = '0.1.0';

export const DEFAULT_PROVIDER = 'claude';
export const DEFAULT_MODEL = 'claude-3-5-sonnet-20240620';

export const DEFAULT_SETTINGS: AppSettings = {
  apiKeys: {},
  defaultModel: DEFAULT_MODEL,
  defaultProvider: DEFAULT_PROVIDER,
  theme: 'dark',
  enginePort: ENGINE_PORT,
  ollamaUrl: 'http://localhost:11434',
};
