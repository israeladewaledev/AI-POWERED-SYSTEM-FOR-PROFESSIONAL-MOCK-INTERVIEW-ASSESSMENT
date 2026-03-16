"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface VideoFeedProps {
  currentQuestion: string;
  isRecording?: boolean;
}

export default function VideoFeed({ currentQuestion, isRecording = false }: VideoFeedProps) {
  return (
    <div className="relative w-full h-full bg-slate-200 dark:bg-slate-800 rounded-2xl overflow-hidden shadow-2xl border border-white/5 group">
      {/* Mock Video Stream Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />

      {/* Fallback/Mock Video Feed */}
      <div className="absolute inset-0 bg-slate-900 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="size-20 bg-primary/20 rounded-full flex items-center justify-center mx-auto ring-4 ring-primary/10">
            <span className="material-symbols-outlined text-primary text-4xl">videocam</span>
          </div>
          <p className="text-slate-400 text-sm font-medium">Camera input active...</p>
        </div>
      </div>

      {/* Actual Webcam Overlay (Placeholder for real stream) */}
      <div className="absolute inset-0 z-0 bg-cover bg-center opacity-70 group-hover:opacity-100 transition-opacity duration-700"
        style={{ backgroundImage: `url('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80')` }}
      />

      {/* Status Indicators */}
      {isRecording && (
        <motion.div
          className="absolute top-6 right-6 flex items-center gap-2 bg-black/40 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 z-20"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="w-2.5 h-2.5 rounded-full bg-danger animate-pulse shadow-[0_0_8px_rgba(255,51,102,0.8)]" />
          <p className="text-xs font-mono font-bold text-white tracking-widest">00:02:14</p>
        </motion.div>
      )}

      {/* Question Overlay Card */}
      <motion.div
        className="absolute top-6 left-6 right-20 z-20"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.3 }}
      >
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-5 rounded-2xl shadow-2xl overflow-hidden relative">
          <div className="absolute top-0 left-0 w-1 h-full bg-primary" />
          <p className="text-white/60 text-[10px] uppercase tracking-[0.2em] mb-1.5 font-black">Current Question</p>
          <p className="text-white text-xl font-medium leading-tight tracking-tight">{currentQuestion}</p>
        </div>
      </motion.div>

      {/* Analysis Pill */}
      <div className="absolute bottom-6 left-6 z-20 flex flex-col gap-2">
        <div className="flex items-center gap-2 bg-primary/20 backdrop-blur-md border border-primary/40 px-3 py-1.5 rounded-full shadow-lg">
          <span className="size-2 rounded-full bg-primary animate-ping" />
          <span className="text-[10px] text-primary font-black uppercase tracking-widest flex items-center gap-1.5">
            <span className="material-symbols-outlined text-xs">mic</span>
            {isRecording ? 'Mic Active' : 'Mic Standby'}
          </span>
        </div>
        <div className="bg-black/40 backdrop-blur-md border border-white/10 px-3 py-1 rounded-full">
          <span className="text-[9px] text-white/60 font-medium uppercase tracking-tighter">Default Input Device</span>
        </div>
      </div>
    </div>
  );
}
