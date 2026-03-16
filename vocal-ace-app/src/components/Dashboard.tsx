"use client";

import React, { useState, useRef } from 'react';
import { Mail, Lock, Eye, History, ArrowRight, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

interface DashboardProps {
  onStartInterview: (resumeText?: string) => void;
}

export default function Dashboard({ onStartInterview }: DashboardProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [resumeParsed, setResumeParsed] = useState(false);
  const [resumeText, setResumeText] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/resume/parse', { method: 'POST', body: formData });
      const data = await response.json();
      if (data.text) {
        setResumeText(data.text);
        setResumeParsed(true);
      }
    } catch (err) {
      console.error('Parsing failed', err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-background-dark text-slate-900 dark:text-white font-sans max-w-md mx-auto relative overflow-x-hidden">
      {/* Top Bar */}
      <div className="flex flex-col items-center gap-1 p-8">
        <div className="text-primary flex size-10 items-center justify-center mb-1">
          <Activity className="size-8" />
        </div>
        <h2 className="text-slate-900 dark:text-white text-2xl font-black tracking-[0.2em] uppercase">VocalAce</h2>
      </div>

      {/* Hero Section */}
      <div className="px-6 pt-4 pb-4 text-center">
        <h2 className="text-slate-900 dark:text-white tracking-tighter text-4xl font-black leading-tight">Master your voice.</h2>
        <p className="text-slate-500 dark:text-slate-400 text-base font-medium transition-colors pt-2">
          {resumeParsed ? 'Resume parsed successfully!' : 'Upload your resume to generate personalized questions.'}
        </p>
      </div>

      {/* Resume Upload Button */}
      <div className="px-6 mt-4">
        <input type="file" className="hidden" ref={fileInputRef} onChange={handleFileChange} accept=".pdf" />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className={`w-full py-8 border-2 border-dashed rounded-3xl flex flex-col items-center gap-3 transition-all ${resumeParsed ? 'border-primary bg-primary/5' : 'border-slate-200 dark:border-white/10 hover:border-primary/50'
            }`}
        >
          {isUploading ? (
            <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="size-8 border-4 border-primary border-t-transparent rounded-full" />
          ) : (
            <span className="material-symbols-outlined text-4xl text-primary">{resumeParsed ? 'check_circle' : 'cloud_upload'}</span>
          )}
          <p className="text-sm font-bold uppercase tracking-widest">{resumeParsed ? 'Resume Ready' : 'Upload Resume'}</p>
        </button>
      </div>

      {/* Login / Start Form */}
      <div className="px-6 space-y-4 mt-8">
        <button
          onClick={() => onStartInterview(resumeText)}
          className="w-full bg-primary hover:bg-primary/90 text-background-dark font-black text-lg h-16 rounded-2xl transition-all active:scale-[0.98] flex items-center justify-center gap-3 shadow-xl shadow-primary/20 group"
        >
          {resumeParsed ? 'Start Personalized Session' : 'Quick Practice Start'}
          <ArrowRight className="size-6 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>

      {/* Vocal Health History */}
      <div className="mt-12 px-6 pb-20">
        <div className="bg-slate-50 dark:bg-slate-800/20 border border-slate-100 dark:border-white/5 rounded-3xl p-6 shadow-sm">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-slate-900 dark:text-white text-lg font-black flex items-center gap-2 uppercase tracking-tight">
              <History className="size-5 text-primary" />
              Recent Progress
            </h3>
            <span className="text-slate-400 text-[10px] font-black uppercase tracking-[0.2em]">Last 30 Days</span>
          </div>

          <div className="grid grid-cols-3 gap-4">
            {[
              { date: 'Oct 12', score: 85, status: 'Confident', color: 'text-primary' },
              { date: 'Oct 08', score: 62, status: 'Strained', color: 'text-warning' },
              { date: 'Oct 03', score: 94, status: 'Optimal', color: 'text-success' }
            ].map((item, idx) => (
              <div key={idx} className="flex flex-col items-center gap-3">
                <div className="relative size-20">
                  <svg className="size-full -rotate-90">
                    <circle cx="40" cy="40" r="36" fill="transparent" stroke="currentColor" strokeWidth="6" className="text-slate-100 dark:text-slate-800" />
                    <motion.circle
                      cx="40" cy="40" r="36" fill="transparent" stroke="currentColor" strokeWidth="6"
                      className="text-primary"
                      strokeDasharray={226.2}
                      initial={{ strokeDashoffset: 226.2 }}
                      animate={{ strokeDashoffset: 226.2 * (1 - item.score / 100) }}
                      transition={{ duration: 1.5, delay: idx * 0.2 }}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center font-black text-xl">{item.score}</div>
                </div>
                <div className="text-center">
                  <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">{item.date}</p>
                  <p className={`text-[9px] ${item.color} uppercase font-black tracking-tighter`}>{item.status}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="pb-10 text-center">
        <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-white/10">
          <span className="size-1.5 rounded-full bg-primary animate-pulse" />
          <span className="text-slate-400 text-[10px] font-black uppercase tracking-[0.3em]">AI-Powered Assessment</span>
        </div>
      </div>
    </div>
  );
}
