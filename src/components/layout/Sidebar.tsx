import * as React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { 
  MessageSquare, 
  Brain, 
  Dna, 
  Box, 
  Settings, 
  PanelLeftClose, 
  PanelLeftOpen 
} from 'lucide-react';
import type { ViewId } from '@/lib/types';

export interface SidebarProps {
  currentView: ViewId;
  collapsed: boolean;
  onNavigate: (view: ViewId) => void;
  onToggle: () => void;
  engineConnected: boolean;
}

const NAV_ITEMS = [
  { id: 'playground' as ViewId, label: 'Playground', icon: MessageSquare },
  { id: 'cortex' as ViewId, label: 'Cortex', icon: Brain },
  { id: 'evolution' as ViewId, label: 'Evolution', icon: Dna },
  { id: 'models' as ViewId, label: 'Models', icon: Box },
  { id: 'settings' as ViewId, label: 'Settings', icon: Settings },
];

export function Sidebar({ currentView, collapsed, onNavigate, onToggle, engineConnected }: SidebarProps) {
  return (
    <motion.div
      initial={false}
      animate={{ width: collapsed ? 64 : 240 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className="relative flex flex-col h-full bg-aether-surface-0/50 backdrop-blur-md border-r border-aether-border shrink-0 z-20"
    >
      {/* Logo Area */}
      <div className="flex h-14 items-center px-4 shrink-0 overflow-hidden">
        <div className="flex items-center gap-3 w-full">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-aether-accent-subtle border border-aether-accent/20 shrink-0 shadow-glow-sm">
            <span className="text-aether-accent font-bold text-lg leading-none tracking-tighter">Æ</span>
          </div>
          <motion.span
            animate={{ opacity: collapsed ? 0 : 1 }}
            transition={{ duration: 0.2 }}
            className="font-semibold text-aether-text-primary tracking-tight whitespace-nowrap"
          >
            Aether
          </motion.span>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 py-4 overflow-y-auto overflow-x-hidden flex flex-col gap-1 px-2 scrollbar-thin">
        {NAV_ITEMS.map((item) => {
          const isActive = currentView === item.id;
          const Icon = item.icon;
          
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={cn(
                "relative flex items-center h-10 w-full rounded-lg transition-all duration-200 group overflow-hidden",
                isActive 
                  ? "bg-aether-surface-1 text-aether-text-primary font-medium" 
                  : "text-aether-text-secondary hover:bg-aether-surface-1/50 hover:text-aether-text-primary"
              )}
              title={collapsed ? item.label : undefined}
            >
              {/* Active Indicator Bar */}
              {isActive && (
                <motion.div 
                  layoutId="activeNav"
                  className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-aether-accent rounded-r-full shadow-glow" 
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              
              <div className="flex items-center justify-center w-10 h-10 shrink-0">
                <Icon className={cn("w-5 h-5 transition-colors", isActive ? "text-aether-accent" : "group-hover:text-aether-text-primary")} />
              </div>
              
              <span className="whitespace-nowrap opacity-100 transition-opacity duration-200">
                {item.label}
              </span>
            </button>
          );
        })}
      </div>

      {/* Footer Area */}
      <div className="p-2 shrink-0 border-t border-aether-border/50">
        <button
          onClick={onToggle}
          className="flex items-center h-10 w-full rounded-lg text-aether-text-secondary hover:bg-aether-surface-1 hover:text-aether-text-primary transition-colors overflow-hidden"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          <div className="flex items-center justify-center w-10 h-10 shrink-0">
            {collapsed ? <PanelLeftOpen className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
          </div>
          <span className="whitespace-nowrap text-sm ml-1 opacity-100 transition-opacity">
            Collapse
          </span>
        </button>
      </div>
    </motion.div>
  );
}
