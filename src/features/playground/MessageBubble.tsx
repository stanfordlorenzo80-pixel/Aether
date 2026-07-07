import * as React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Copy, Bot } from 'lucide-react';
import type { Message } from '@/lib/types';

// Extremely basic markdown renderer for now
const renderMarkdown = (text: string) => {
  // Replace code blocks
  let html = text.replace(/```([\s\S]*?)```/g, '<pre class="bg-aether-surface-2 p-3 rounded-md my-2 overflow-x-auto border border-aether-border/50 text-xs text-aether-accent-secondary"><code>$1</code></pre>');
  // Replace inline code
  html = html.replace(/`([^`]+)`/g, '<code class="bg-aether-surface-2 text-aether-accent-secondary px-1.5 py-0.5 rounded text-xs">$1</code>');
  // Replace bold
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Replace italic
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  // Handle line breaks
  html = html.replace(/\n/g, '<br/>');
  return html;
};

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn("flex w-full mb-6", isUser ? "justify-end" : "justify-start")}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-aether-accent/10 border border-aether-accent/20 flex items-center justify-center mr-3 mt-1 shrink-0">
          <Bot className="w-4 h-4 text-aether-accent" />
        </div>
      )}

      <div className={cn(
        "relative group max-w-[80%] rounded-2xl px-5 py-3.5 text-[15px] leading-relaxed",
        isUser 
          ? "bg-aether-surface-1/50 border border-aether-border text-aether-text-primary rounded-tr-sm" 
          : "bg-transparent text-aether-text-primary"
      )}>
        <div 
          className="prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }} 
        />
        
        {message.isStreaming && (
          <span className="inline-block w-2 h-4 bg-aether-accent ml-1 animate-pulse align-middle" />
        )}

        {/* Action button container */}
        {!isUser && !message.isStreaming && (
          <div className="absolute top-2 -right-10 opacity-0 group-hover:opacity-100 transition-opacity">
            <button 
              onClick={handleCopy}
              className="p-1.5 text-aether-text-tertiary hover:text-aether-text-primary bg-aether-surface-0 rounded-md border border-aether-border"
              title="Copy"
            >
              <Copy className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Footer info */}
        <div className={cn(
          "flex items-center gap-2 mt-2 text-[10px] text-aether-text-tertiary select-none",
          isUser ? "justify-end" : "justify-start"
        )}>
          {message.tokens && (
            <span>{message.tokens} tokens</span>
          )}
          {message.latency && (
            <span>{message.latency}ms</span>
          )}
        </div>
      </div>
    </motion.div>
  );
}
