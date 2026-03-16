"use client";

import React from 'react';
import { ChevronLeft, Settings, User } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function InterviewHeader() {
  const router = useRouter();

  return (
    <header className="flex items-center bg-white dark:bg-background-dark p-4 justify-between sticky top-0 z-50 border-b border-slate-100 dark:border-white/5">
      <div className="flex items-center gap-4">
        <button
          onClick={() => router.push('/')}
          className="flex size-10 shrink-0 items-center justify-center rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <ChevronLeft className="size-5" />
        </button>
        <div>
          <h2 className="text-slate-900 dark:text-white text-sm font-black leading-tight uppercase tracking-[0.2em]">VocalAce Simulation</h2>
          <p className="text-[10px] text-primary font-bold uppercase tracking-widest mt-0.5">Mock Interview Session</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button className="flex items-center justify-center rounded-xl h-10 w-10 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-primary/20 hover:text-primary transition-all">
          <Settings className="size-5" />
        </button>
        <div className="w-px h-6 bg-slate-200 dark:bg-white/10 mx-1" />
        <button className="flex items-center gap-2 pl-1 pr-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-white/5">
          <div className="size-8 rounded-full bg-primary/20 flex items-center justify-center text-primary">
            <User className="size-4" />
          </div>
          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">Candidate</span>
        </button>
      </div>
    </header>
  );
}
