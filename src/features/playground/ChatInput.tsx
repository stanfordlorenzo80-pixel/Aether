import * as React from 'react';
import { cn } from '@/lib/utils';
import { ArrowUp, Square } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export interface ChatInputProps {
  onSend: (text: string) => void;
  isStreaming: boolean;
  onStop: () => void;
}

export function ChatInput({ onSend, isStreaming, onStop }: ChatInputProps) {
  const [text, setText] = React.useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const adjustHeight = () => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (text.trim() && !isStreaming) {
        onSend(text.trim());
        setText('');
        if (textareaRef.current) {
          textareaRef.current.style.height = 'auto';
        }
      }
    }
  };

  return (
    <div className="relative w-full max-w-3xl mx-auto">
      <div className="relative flex items-end w-full bg-aether-surface-1 border border-aether-border rounded-xl shadow-surface-1 transition-colors focus-within:border-aether-border-focus focus-within:ring-1 focus-within:ring-aether-border-focus overflow-hidden">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            adjustHeight();
          }}
          onKeyDown={handleKeyDown}
          placeholder="Ask Aether anything..."
          className="w-full max-h-[200px] bg-transparent border-0 py-4 pl-4 pr-14 text-sm text-aether-text-primary placeholder:text-aether-text-tertiary focus:ring-0 resize-none scrollbar-thin"
          rows={1}
          disabled={isStreaming}
        />
        
        <div className="absolute right-2 bottom-2">
          <AnimatePresence mode="wait">
            {isStreaming ? (
              <motion.button
                key="stop"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                onClick={onStop}
                className="flex items-center justify-center w-8 h-8 rounded-lg bg-aether-surface-2 text-aether-text-primary hover:bg-aether-border transition-colors"
              >
                <Square className="w-3.5 h-3.5 fill-current" />
              </motion.button>
            ) : text.trim() ? (
              <motion.button
                key="send"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                onClick={() => {
                  onSend(text.trim());
                  setText('');
                  if (textareaRef.current) textareaRef.current.style.height = 'auto';
                }}
                className="flex items-center justify-center w-8 h-8 rounded-lg bg-aether-accent text-white hover:bg-aether-accent-hover shadow-glow-sm transition-colors"
              >
                <ArrowUp className="w-4 h-4" />
              </motion.button>
            ) : null}
          </AnimatePresence>
        </div>
      </div>
      <div className="text-center mt-2">
        <span className="text-[10px] text-aether-text-tertiary">Aether Engine Alpha. Models may produce inaccurate info.</span>
      </div>
    </div>
  );
}
