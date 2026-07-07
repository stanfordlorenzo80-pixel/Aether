import * as React from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { StatusBar } from './components/layout/StatusBar';

import { PlaygroundView } from './features/playground/PlaygroundView';
import { ModelsView } from './features/models/ModelsView';
import { SettingsView } from './features/settings/SettingsView';
import { CortexView } from './features/cortex/CortexView';
import { EvolutionView } from './features/evolution/EvolutionView';

import { useAether, useTheme } from './lib/hooks';
import { useUIStore } from './lib/store';

export default function App() {
  // Initialize theme
  useTheme();
  
  // Connect to engine
  const { connected, latency } = useAether();
  
  // Get UI state
  const { currentView, setCurrentView, sidebarCollapsed, toggleSidebar } = useUIStore();

  // Render current view
  const renderView = () => {
    switch (currentView) {
      case 'playground':
        return <PlaygroundView />;
      case 'cortex':
        return <CortexView />;
      case 'evolution':
        return <EvolutionView />;
      case 'models':
        return <ModelsView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <PlaygroundView />;
    }
  };

  // Get title for current view
  const getViewTitle = () => {
    switch (currentView) {
      case 'playground': return 'Playground';
      case 'cortex': return 'Cortex Graph';
      case 'evolution': return 'System Evolution';
      case 'models': return 'Models & Providers';
      case 'settings': return 'Settings';
      default: return 'Aether';
    }
  };

  return (
    <div className="flex h-screen w-full bg-aether-bg text-aether-text-primary overflow-hidden selection:bg-aether-accent-glow">
      <Sidebar 
        currentView={currentView}
        collapsed={sidebarCollapsed}
        onNavigate={setCurrentView}
        onToggle={toggleSidebar}
        engineConnected={connected}
      />
      
      <div className="flex flex-col flex-1 min-w-0 h-full relative">
        <Header title={getViewTitle()} connected={connected} />
        
        <main className="flex-1 overflow-hidden relative">
          {renderView()}
        </main>
        
        <StatusBar connected={connected} latency={latency} />
      </div>
    </div>
  );
}
