"use client";

import React from 'react';
import { Square, Pause, Play, Edit3, Save, Share2 } from 'lucide-react';

interface RecordingControlsProps {
  isRecording: boolean;
  onStop: () => void;
  onPause: () => void;
  onEdit: () => void;
  onSave: () => void;
  onShare: () => void;
}

export default function RecordingControls({
  isRecording,
  onStop,
  onPause,
  onEdit,
  onSave,
  onShare
}: RecordingControlsProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white/80 dark:bg-background-dark/80 backdrop-blur-xl border-t border-slate-200 dark:border-white/10 p-6 z-50">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Recording Controls */}
        <div className="flex items-center gap-4">
          <button
            onClick={onStop}
            className="group flex items-center gap-3 bg-danger hover:bg-danger/90 text-white font-black py-4 px-8 rounded-2xl transition-all shadow-xl shadow-danger/20 hover:scale-[1.02] active:scale-95"
          >
            <Square className="size-5 fill-white" />
            <span className="uppercase tracking-widest text-xs">Stop Interview</span>
          </button>

          <button
            onClick={onPause}
            className="size-14 flex items-center justify-center bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-2xl hover:bg-slate-200 dark:hover:bg-slate-700 transition-all border border-slate-200 dark:border-white/5"
          >
            {isRecording ? <Pause className="size-6" /> : <Play className="size-6" />}
          </button>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 md:gap-6">
          <button onClick={onEdit} className="flex flex-col items-center gap-1 group">
            <div className="size-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 group-hover:bg-primary/20 group-hover:text-primary transition-all">
              <Edit3 className="size-5" />
            </div>
            <span className="text-[10px] font-bold uppercase text-slate-400">Edit</span>
          </button>

          <button onClick={onSave} className="flex flex-col items-center gap-1 group">
            <div className="size-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 group-hover:bg-success/20 group-hover:text-success transition-all">
              <Save className="size-5" />
            </div>
            <span className="text-[10px] font-bold uppercase text-slate-400">Save</span>
          </button>

          <div className="w-px h-8 bg-slate-200 dark:bg-white/10 mx-2" />

          <button onClick={onShare} className="flex flex-col items-center gap-1 group">
            <div className="size-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 group-hover:bg-blue-500/20 group-hover:text-blue-500 transition-all">
              <Share2 className="size-5" />
            </div>
            <span className="text-[10px] font-bold uppercase text-slate-400">Share</span>
          </button>
        </div>
      </div>
    </div>
  );
}
