import React from 'react';

export default function RiskGauge({ probabilities }) {
  if (!probabilities) return null;

  const entries = Object.entries(probabilities);

  return (
    <div className="w-full h-full flex flex-col">
      <h3 className="text-slate-300 font-medium mb-4 px-2 text-sm uppercase tracking-wider">AI Diagnostic Confidence</h3>
      <div className="flex-1 flex flex-col justify-center gap-4 px-2">
        {entries.map(([cls, prob]) => {
          const score = prob * 100;
          return (
            <div key={cls} className="flex flex-col gap-1.5">
              <div className="flex justify-between text-sm">
                <span className="text-slate-300">{cls}</span>
                <span className="text-slate-400 font-mono">{score.toFixed(1)}%</span>
              </div>
              <div className="w-full h-3 bg-navy-900 rounded-full overflow-hidden border border-navy-700/50">
                <div 
                  className={`h-full rounded-full transition-all duration-1000 ${score > 50 ? 'bg-teal-accent' : 'bg-navy-600'}`}
                  style={{ width: `${Math.max(score, 1)}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
