import { useState, useRef, useCallback } from 'react';
import { ENGINE_URL } from '@/lib/constants';
import type { StreamChunk, Message } from '@/lib/types';

interface UseStreamOptions {
  onChunk: (chunk: string) => void;
  onDone?: () => void;
  onError?: (error: string) => void;
}

export function useStream() {
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const startStream = useCallback(async (
    messages: Omit<Message, 'id' | 'timestamp'>[],
    model: string,
    options: UseStreamOptions
  ) => {
    if (isStreaming) return;
    
    setIsStreaming(true);
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${ENGINE_URL}/api/chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, model, stream: true }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Response body is null');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          options.onDone?.();
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        
        // Process complete SSE messages
        let newlineIndex;
        while ((newlineIndex = buffer.indexOf('\n\n')) >= 0) {
          const message = buffer.slice(0, newlineIndex);
          buffer = buffer.slice(newlineIndex + 2);
          
          if (message.startsWith('data: ')) {
            const dataStr = message.slice(6);
            if (dataStr === '[DONE]') {
              continue;
            }
            
            try {
              const chunk: StreamChunk = JSON.parse(dataStr);
              if (chunk.type === 'content' && chunk.content) {
                options.onChunk(chunk.content);
              } else if (chunk.type === 'error') {
                options.onError?.(chunk.error || 'Unknown error from engine');
              } else if (chunk.type === 'done') {
                // Done event
              }
            } catch (e) {
              console.error('Failed to parse SSE chunk', e);
            }
          }
        }
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.log('Stream aborted');
        options.onDone?.(); // Call onDone even on abort to clean up state
      } else {
        options.onError?.(err.message || 'Streaming failed');
      }
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  }, [isStreaming]);

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  return { startStream, stopStream, isStreaming };
}
