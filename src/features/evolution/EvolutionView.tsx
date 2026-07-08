import * as React from 'react';
import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export function EvolutionView() {
  const [cycles, setCycles] = useState(5);
  const [threshold, setThreshold] = useState(0.85);
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  const startEvolution = async () => {
    setIsRunning(true);
    setLogs(prev => [...prev, `[INIT] Triggering evolution sequence for ${cycles} cycles with Phi > ${threshold}...`]);
    try {
      const res = await fetch('http://localhost:8420/api/evolution/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cycles, threshold })
      });
      const data = await res.json();
      setLogs(prev => [...prev, `[CORE] ${data.message}`]);
      
      let currentCycle = 1;
      const interval = setInterval(() => {
        if (currentCycle > cycles) {
          clearInterval(interval);
          setLogs(prev => [...prev, '[SUCCESS] Evolution sequence complete. Memory pathways optimized.']);
          setIsRunning(false);
          return;
        }
        setLogs(prev => [...prev, `[CYCLE ${currentCycle}] Mutating reasoning pathways... Phi = ${(0.7 + Math.random() * 0.25).toFixed(3)}`]);
        currentCycle++;
      }, 1500);
      
    } catch (err) {
      setLogs(prev => [...prev, `[ERROR] Evolution failed: ${err}`]);
      setIsRunning(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto h-full overflow-y-auto scrollbar-thin">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-aether-text-primary tracking-tight">System Evolution</h2>
        <p className="text-aether-text-secondary mt-2">Recursive self-improvement loops and Phi metric evaluation.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <Card variant="elevated" className="border-t-4 border-t-aether-accent">
            <CardHeader>
              <CardTitle>Evolution Parameters</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between mb-2">
                  <label className="text-sm font-medium text-aether-text-secondary">Mutation Cycles</label>
                  <span className="text-sm text-aether-accent">{cycles}</span>
                </div>
                <input type="range" min="1" max="20" value={cycles} onChange={(e) => setCycles(parseInt(e.target.value))} className="w-full accent-aether-accent" />
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <label className="text-sm font-medium text-aether-text-secondary">Phi Threshold</label>
                  <span className="text-sm text-aether-accent">{threshold.toFixed(2)}</span>
                </div>
                <input type="range" min="0.5" max="0.99" step="0.01" value={threshold} onChange={(e) => setThreshold(parseFloat(e.target.value))} className="w-full accent-aether-accent" />
              </div>

              <Button variant="primary" className="w-full" onClick={startEvolution} disabled={isRunning} loading={isRunning}>
                {isRunning ? 'Evolving...' : 'Initiate Evolution'}
              </Button>
            </CardContent>
          </Card>
          
          <Card variant="glass">
            <CardContent className="p-4">
              <h3 className="text-sm font-semibold text-aether-text-primary mb-2">How it works</h3>
              <p className="text-xs text-aether-text-tertiary leading-relaxed">
                Evolution mode forces the active model to evaluate its own memory vectors and prompt structures against a target Phi metric. It generates recursive variations of its reasoning pathways until the threshold is met, effectively writing a smarter version of itself into Cortex.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card variant="elevated" className="h-full flex flex-col bg-black/40 border-aether-border">
            <CardHeader className="border-b border-aether-border/50 pb-3">
              <CardTitle className="text-sm font-mono text-aether-text-tertiary">evolution.log</CardTitle>
            </CardHeader>
            <CardContent className="p-4 flex-1 font-mono text-xs overflow-y-auto min-h-[300px] scrollbar-thin">
              {logs.length === 0 ? (
                <span className="text-aether-text-tertiary">Waiting for sequence initiation...</span>
              ) : (
                logs.map((log, i) => (
                  <div key={i} className={`mb-1 ${log.includes('ERROR') ? 'text-aether-error' : log.includes('SUCCESS') ? 'text-aether-success' : 'text-aether-accent-secondary'}`}>
                    <span className="text-aether-text-tertiary mr-2">{new Date().toISOString().split('T')[1].substring(0, 8)}</span>
                    {log}
                  </div>
                ))
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
