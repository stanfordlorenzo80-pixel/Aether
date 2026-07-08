import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { persist } from 'zustand/middleware';
import type { Conversation, Message, ProviderInfo, EngineStatus, ViewId } from './types';

// Chat Store
interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  isStreaming: boolean;
  createConversation: (model: string) => string;
  addMessage: (convId: string, message: Message) => void;
  updateMessage: (convId: string, msgId: string, updates: Partial<Message>) => void;
  setStreaming: (isStreaming: boolean) => void;
  setActiveConversation: (id: string | null) => void;
  getActiveConversation: () => Conversation | undefined;
}

export const useChatStore = create<ChatState>()(
  persist(
    immer((set, get) => ({
      conversations: [],
      activeConversationId: null,
      isStreaming: false,
    
    createConversation: (model) => {
      const id = crypto.randomUUID();
      const newConv: Conversation = {
        id,
        title: 'New Conversation',
        messages: [],
        model,
        createdAt: Date.now(),
        updatedAt: Date.now(),
      };
      set((state) => {
        state.conversations.unshift(newConv);
        state.activeConversationId = id;
      });
      return id;
    },
    
    addMessage: (convId, message) => {
      set((state) => {
        const conv = state.conversations.find((c) => c.id === convId);
        if (conv) {
          conv.messages.push(message);
          conv.updatedAt = Date.now();
          if (conv.messages.length === 2) {
            // Auto-generate title from first user message
            const firstUserMsg = conv.messages.find(m => m.role === 'user');
            if (firstUserMsg) {
              conv.title = firstUserMsg.content.slice(0, 30) + (firstUserMsg.content.length > 30 ? '...' : '');
            }
          }
        }
      });
    },
    
    updateMessage: (convId, msgId, updates) => {
      set((state) => {
        const conv = state.conversations.find((c) => c.id === convId);
        if (conv) {
          const msg = conv.messages.find((m) => m.id === msgId);
          if (msg) {
            Object.assign(msg, updates);
            conv.updatedAt = Date.now();
          }
        }
      });
    },
    
    setStreaming: (isStreaming) => {
      set((state) => {
        state.isStreaming = isStreaming;
      });
    },
    
    setActiveConversation: (id) => {
      set((state) => {
        state.activeConversationId = id;
      });
    },
    
    getActiveConversation: () => {
      const { conversations, activeConversationId } = get();
      return conversations.find((c) => c.id === activeConversationId);
    },
  })),
  {
    name: 'aether-chat-storage',
    partialize: (state) => ({ 
      conversations: state.conversations, 
      activeConversationId: state.activeConversationId 
    }),
  }
)
);

// Model Store
interface ModelState {
  providers: ProviderInfo[];
  activeProvider: string;
  activeModel: string;
  isConnected: boolean;
  setProviders: (providers: ProviderInfo[]) => void;
  setActiveModel: (provider: string, model: string) => void;
  setConnectionStatus: (isConnected: boolean) => void;
}

export const useModelStore = create<ModelState>()(
  persist(
    immer((set) => ({
      providers: [],
      activeProvider: 'claude',
      activeModel: 'claude-3-5-sonnet-20240620',
      isConnected: false,
    
    setProviders: (providers) => {
      set((state) => {
        state.providers = providers;
      });
    },
    
    setActiveModel: (provider, model) => {
      set((state) => {
        state.activeProvider = provider;
        state.activeModel = model;
      });
    },
    
    setConnectionStatus: (isConnected) => {
      set((state) => {
        state.isConnected = isConnected;
      });
    },
  })),
  {
    name: 'aether-model-storage',
    partialize: (state) => ({ 
      activeProvider: state.activeProvider, 
      activeModel: state.activeModel 
    }),
  }
)
);

// UI Store
interface UIState {
  sidebarCollapsed: boolean;
  currentView: ViewId;
  engineStatus: EngineStatus | null;
  toggleSidebar: () => void;
  setCurrentView: (view: ViewId) => void;
  setEngineStatus: (status: EngineStatus) => void;
}

export const useUIStore = create<UIState>()(
  immer((set) => ({
    sidebarCollapsed: false,
    currentView: 'playground',
    engineStatus: null,
    
    toggleSidebar: () => {
      set((state) => {
        state.sidebarCollapsed = !state.sidebarCollapsed;
      });
    },
    
    setCurrentView: (view) => {
      set((state) => {
        state.currentView = view;
      });
    },
    
    setEngineStatus: (status) => {
      set((state) => {
        state.engineStatus = status;
      });
    },
  }))
);
