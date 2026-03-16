"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Info, Lightbulb } from 'lucide-react';

interface AnalysisSidebarProps {
  confidence: number;
  transcript: { speaker: string; text: string }[];
  isAnalyzing?: boolean;
}

export default function AnalysisSidebar({ confidence, transcript, isAnalyzing = true }: AnalysisSidebarProps) {
  return (
    <aside className="w-full lg:w-96 flex flex-col gap-6 bg-slate-50 dark:bg-slate-900/50 p-6 rounded-2xl border border-slate-200 dark:border-white/10 overflow-hidden h-full">
      {/* Module 1: Maryam's Speech-to-Tone Analysis */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-slate-400">Vocal Confidence Analysis</h3>
          <Info className="size-4 text-primary" />
        </div>
        
        <div className="grid grid-cols-12 gap-4 bg-white dark:bg-slate-800/20 p-4 rounded-xl border border-slate-200 dark:border-white/5 shadow-sm">
          {/* Vertical Confidence Meter */}
          <div className="col-span-3 flex flex-col items-center gap-2">
            <div className="relative w-4 h-32 bg-slate-200 dark:bg-slate-700/50 rounded-full overflow-hidden flex flex-col-reverse">
              <motion.div 
                className="w-full bg-gradient-to-t from-danger via-warning to-success transition-all duration-500"
                initial={{ height: 0 }}
                animate={{ height: `${confidence}%` }}
              />
              <motion.div 
                className="absolute left-0 w-full h-1 bg-white shadow-[0_0_10px_rgba(255,255,255,0.8)] z-10"
                animate={{ bottom: `${confidence}%` }}
              />
            </div>
            <p className="text-[9px] font-bold text-slate-400 uppercase">Level</p>
          </div>
          
          <div className="col-span-9 flex flex-col justify-between py-1">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-4xl font-bold text-slate-900 dark:text-white font-display tracking-tight">{confidence}%</p>
                <p className="text-[10px] text-success font-bold uppercase tracking-tight">Confidence Score</p>
              </div>
            </div>
            
            <div className="mt-4">
              <div className="flex items-end justify-between h-10 w-full gap-1">
                {[...Array(12)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="w-1.5 bg-primary/40 rounded-full"
                    animate={{ 
                      height: [10, isAnalyzing ? (Math.random() * 40 + 10) : 10, 10], 
                      backgroundColor: isAnalyzing ? '#00d6ab66' : '#94a3b833' 
                    }}
                    transition={{ repeat: Infinity, duration: 1.5, delay: i * 0.1 }}
                  />
                ))}
              </div>
              <p className="text-[9px] text-slate-400 mt-2 text-center uppercase tracking-widest font-bold">Acoustic Signal</p>
            </div>
          </div>
        </div>
      </section>

      {/* Module 2: Firdausi's Speech-to-Text Transcription */}
      <section className="flex-1 flex flex-col min-h-0 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-slate-400">Live Transcript</h3>
          {isAnalyzing && (
            <span className="flex items-center gap-1.5 text-[9px] bg-primary/10 text-primary px-2 py-1 rounded-full font-bold uppercase ring-1 ring-primary/20">
              <span className="size-1.5 rounded-full bg-primary animate-pulse" />
              Processing
            </span>
          )}
        </div>

        <div className="flex-1 bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 rounded-xl p-4 overflow-hidden flex flex-col">
          <div className="flex-1 overflow-y-auto space-y-4 font-mono text-[13px] leading-relaxed pr-2">
            {transcript.map((line, idx) => (
              <div key={idx} className="space-y-1">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{line.speaker}</p>
                <p className={line.speaker === 'Candidate' ? 'text-slate-900 dark:text-slate-100' : 'text-slate-400 italic'}>
                  {line.text}
                </p>
              </div>
            ))}
            {isAnalyzing && (
              <motion.div 
                className="inline-block w-2 h-4 bg-primary align-middle"
                animate={{ opacity: [1, 0] }}
                transition={{ repeat: Infinity, duration: 0.8 }}
              />
            )}
          </div>
        </div>
      </section>

      {/* Unified AI Insights */}
      <section className="bg-primary/5 dark:bg-primary/10 border border-primary/20 p-4 rounded-xl">
        <div className="flex items-center gap-3 mb-2">
          <Lightbulb className="size-4 text-primary" />
          <h4 className="text-xs font-bold uppercase tracking-widest text-primary">AI Coach Insight</h4>
        </div>
        <p className="text-[11px] text-slate-600 dark:text-slate-300 leading-snug">
          Your energy is stable, but I detected filler words. Try pausing briefly instead of using fillers to maintain 90%+ confidence.
        </p>
      </section>
    </aside>
  );
}
