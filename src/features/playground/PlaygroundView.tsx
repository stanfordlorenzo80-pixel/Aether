import * as React from 'react';
import { motion } from 'framer-motion';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { useChatStore, useModelStore } from '@/lib/store';
import { useStream } from '@/lib/hooks';
import { Card } from '@/components/ui/Card';
import { Zap, Code, Layout } from 'lucide-react';
import type { Message } from '@/lib/types';

export function PlaygroundView() {
  const { 
    conversations, 
    activeConversationId, 
    createConversation, 
    addMessage, 
    updateMessage,
    getActiveConversation
  } = useChatStore();
  
  const activeModel = useModelStore(state => state.activeModel);
  const { startStream, stopStream, isStreaming } = useStream();
  
  const scrollRef = React.useRef<HTMLDivElement>(null);
  
  const conversation = getActiveConversation();
  const messages = conversation?.messages || [];

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (text: string) => {
    let convId = activeConversationId;
    if (!convId) {
      convId = createConversation(activeModel);
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: Date.now()
    };
    addMessage(convId, userMessage);

    const assistantMsgId = crypto.randomUUID();
    const assistantMessage: Message = {
      id: assistantMsgId,
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isStreaming: true,
      model: activeModel
    };
    addMessage(convId, assistantMessage);

    // Prepare history for API
    const conv = useChatStore.getState().conversations.find(c => c.id === convId);
    if (!conv) return;
    
    // Omit the newly created empty assistant message
    const apiMessages = conv.messages
      .filter(m => m.id !== assistantMsgId)
      .map(m => ({ role: m.role, content: m.content }));

    await startStream(apiMessages, activeModel, {
      onChunk: (chunkText) => {
        const currentMsg = useChatStore.getState()
          .conversations.find(c => c.id === convId)
          ?.messages.find(m => m.id === assistantMsgId);
          
        if (currentMsg) {
          updateMessage(convId!, assistantMsgId, {
            content: currentMsg.content + chunkText
          });
        }
      },
      onDone: () => {
        updateMessage(convId!, assistantMsgId, { isStreaming: false });
      },
      onError: (err) => {
        updateMessage(convId!, assistantMsgId, { 
          isStreaming: false,
          content: useChatStore.getState()
            .conversations.find(c => c.id === convId)
            ?.messages.find(m => m.id === assistantMsgId)?.content + `\n\n**Error:** ${err}`
        });
      }
    });
  };

  return (
    <div className="flex flex-col h-full bg-transparent">
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-6 py-8 scrollbar-thin"
      >
        <div className="max-w-3xl mx-auto">
          {messages.length === 0 ? (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center justify-center pt-20 pb-10 text-center"
            >
              <div className="w-16 h-16 rounded-2xl bg-aether-accent-subtle border border-aether-accent/20 flex items-center justify-center mb-6 shadow-glow">
                <span className="text-aether-accent font-bold text-4xl leading-none tracking-tighter">Æ</span>
              </div>
              <h2 className="text-2xl font-semibold text-aether-text-primary mb-2 tracking-tight">Think beyond.</h2>
              <p className="text-aether-text-secondary max-w-md mx-auto mb-12">
                Aether connects seamlessly to Claude and local models via Ollama. How can I help you today?
              </p>

              <div className="grid grid-cols-3 gap-4 w-full max-w-2xl text-left">
                {[
                  { icon: Zap, text: "Explain quantum entanglement simply" },
                  { icon: Code, text: "Write a recursive Fibonacci in Rust" },
                  { icon: Layout, text: "Compare transformer vs state-space architectures" }
                ].map((item, i) => (
                  <Card 
                    key={i} 
                    glowOnHover 
                    variant="elevated"
                    className="p-4 cursor-pointer"
                    onClick={() => handleSend(item.text)}
                  >
                    <item.icon className="w-5 h-5 text-aether-accent mb-3 opacity-80" />
                    <p className="text-sm text-aether-text-primary leading-snug">{item.text}</p>
                  </Card>
                ))}
              </div>
            </motion.div>
          ) : (
            <div className="pb-4">
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="shrink-0 p-4 bg-gradient-to-t from-aether-bg to-transparent">
        <ChatInput 
          onSend={handleSend} 
          isStreaming={isStreaming} 
          onStop={stopStream} 
        />
      </div>
    </div>
  );
}
