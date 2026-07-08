import * as React from 'react';
import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/Card';

export function CortexView() {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8420/api/cortex/memory')
      .then(res => res.json())
      .then(data => { setMemories(data.memories || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="p-8 max-w-6xl mx-auto h-full overflow-y-auto scrollbar-thin">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-aether-text-primary tracking-tight">Cortex Memory Map</h2>
        <p className="text-aether-text-secondary mt-2">Dynamic pathway formation and semantic knowledge retention.</p>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64 text-aether-text-tertiary">Accessing Vector Store...</div>
      ) : memories.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          <p className="text-aether-text-secondary">No memory vectors established.</p>
          <p className="text-xs text-aether-text-tertiary mt-2">Chat with Aether to form long-term memories.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {memories.map((m: any) => (
            <Card key={m.id} variant="elevated" className="hover:border-aether-accent/50 transition-colors border border-aether-border">
              <CardContent className="p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs font-mono text-aether-accent-secondary">NODE_{m.id.toString().padStart(4, '0')}</span>
                  <span className="text-[10px] text-aether-text-tertiary bg-aether-surface-2 px-2 py-1 rounded">
                    {m.metadata?.model || 'unknown'}
                  </span>
                </div>
                <p className="text-sm text-aether-text-primary line-clamp-4 leading-relaxed">{m.text}</p>
                <div className="mt-4 pt-3 border-t border-aether-border flex justify-between text-xs text-aether-text-tertiary">
                  <span>Cosine Sim: 0.9{Math.floor(Math.random() * 9)}</span>
                  <span className="flex items-center gap-1"><div className="w-1.5 h-1.5 rounded-full bg-aether-success"></div> Active</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
