"use client";

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Share2, RefreshCw, Download, Zap, TrendingUp, Search, Clock, Award, Lightbulb, MessageSquare, Loader2 } from 'lucide-react';
import { useInterview } from '@/context/InterviewContext';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { useRef } from 'react';

interface PerformanceReportProps {
  onRestart: () => void;
}

export default function PerformanceReport({ onRestart }: PerformanceReportProps) {
  const { confidence, confidenceHistory, transcript, analysis, setAnalysis } = useInterview();
  const reportRef = useRef<HTMLDivElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const score = confidence || 84;

  useEffect(() => {
    if (transcript.length > 1 && !analysis && !isGenerating) {
      generateAnalysis();
    }
  }, [transcript]);

  const generateAnalysis = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch('/api/interview/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, confidenceHistory })
      });
      const data = await res.json();
      if (data.feedback) {
        setAnalysis(data.feedback);
      }
    } catch (err) {
      console.error("Analysis failed", err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;

    const canvas = await html2canvas(reportRef.current, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff'
    });

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(`VocalAce_Report_${new Date().toLocaleDateString()}.pdf`);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-background-dark text-slate-900 dark:text-white font-sans max-w-2xl mx-auto pb-40" ref={reportRef}>
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md p-6 border-b border-slate-200 dark:border-white/5 flex items-center justify-between">
        <h1 className="text-lg font-black uppercase tracking-widest">Performance Analysis</h1>
        <button className="size-10 flex items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
          <Share2 className="size-5" />
        </button>
      </header>

      <main className="p-6 space-y-8">
        {/* Main Score & Title */}
        <div className="text-center space-y-6">
          <div className="space-y-1">
            <h2 className="text-3xl font-black tracking-tighter">Interview Report</h2>
            <p className="text-slate-500 dark:text-primary/70 text-xs font-black uppercase tracking-widest">October 24, 2023 • 15:20 Duration</p>
          </div>

          <div className="relative w-56 h-56 mx-auto flex items-center justify-center">
            <svg className="size-full -rotate-90">
              <circle cx="112" cy="112" r="100" fill="transparent" stroke="currentColor" strokeWidth="12" className="text-slate-100 dark:text-slate-800" />
              <motion.circle
                cx="112" cy="112" r="100" fill="transparent" stroke="currentColor" strokeWidth="12"
                className="text-primary"
                strokeDasharray={628.3}
                initial={{ strokeDashoffset: 628.3 }}
                animate={{ strokeDashoffset: 628.3 * (1 - score / 100) }}
                transition={{ duration: 2, ease: "easeOut" }}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-6xl font-black tracking-tighter">{score}<span className="text-2xl">%</span></span>
              <span className="text-[10px] uppercase tracking-[0.2em] font-black text-slate-400 mt-1">Overall Confidence</span>
            </div>
          </div>

          <div className="inline-flex items-center gap-2 px-6 py-2 bg-primary/10 text-primary rounded-full text-xs font-black border border-primary/20 uppercase tracking-widest">
            <Award className="size-4" />
            Excellent Performance
          </div>
        </div>

        {/* Pitch Variability Graph */}
        <section className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 p-6 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="font-black text-sm uppercase tracking-widest text-slate-500">Pitch Variability</h3>
            <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Hertz / Time</span>
          </div>

          <div className="relative h-32 w-full">
            <svg className="w-full h-full overflow-visible" viewBox="0 0 400 100">
              <defs>
                <linearGradient id="line-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#00ff80" />
                  <stop offset="50%" stopColor="#ffcc00" />
                  <stop offset="100%" stopColor="#ff3366" />
                </linearGradient>
              </defs>
              <motion.path
                d={confidenceHistory.length > 1
                  ? `M ${confidenceHistory.map((val, i) => `${(i / (confidenceHistory.length - 1)) * 400},${100 - val}`).join(' L ')}`
                  : "M 0 50 L 400 50" // Fallback line
                }
                fill="none"
                stroke="url(#line-gradient)"
                strokeWidth="3"
                strokeLinecap="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, ease: "easeInOut" }}
              />
            </svg>
            <div className="flex justify-between mt-4 text-[9px] font-black text-slate-400 uppercase tracking-[0.2em]">
              <span>Start</span>
              <span>Mid-Interview</span>
              <span>End</span>
            </div>
          </div>
        </section>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4">
          {[
            { label: 'Avg Energy', value: '68dB', icon: Zap, detail: 'Consistent', color: 'text-primary' },
            { label: 'Filler Words', value: '12', icon: MessageSquare, detail: 'Slightly high', color: 'text-warning' },
            { label: 'Interview Pace', value: '142wpm', icon: TrendingUp, detail: 'Optimal', color: 'text-primary' },
            { label: 'Sentiment', value: 'Positive', icon: Search, detail: '94% Accuracy', color: 'text-success' }
          ].map((item, idx) => (
            <div key={idx} className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 p-4 rounded-2xl flex flex-col justify-between aspect-square transition-transform hover:scale-[1.02]">
              <div className="flex justify-between items-start">
                <item.icon className={`size-5 ${item.color}`} />
                <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest">{item.label}</span>
              </div>
              <div>
                <div className="text-3xl font-black mb-1">{item.value}</div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tight">{item.detail}</p>
              </div>
            </div>
          ))}
        </div>

        {/* AI Insight Card */}
        <section className="bg-primary/5 dark:bg-primary/10 border border-primary/20 p-6 rounded-3xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Lightbulb className="size-20 text-primary" />
          </div>
          <div className="flex items-center gap-3 mb-4">
            <div className={`size-10 rounded-2xl bg-primary flex items-center justify-center text-background-dark shadow-lg shadow-primary/20 ${isGenerating ? 'animate-pulse' : ''}`}>
              {isGenerating ? <Loader2 className="size-6 animate-spin" /> : <Lightbulb className="size-6" />}
            </div>
            <h4 className="font-black uppercase tracking-widest text-primary">
              {isGenerating ? 'Gemini AI Analyzing...' : 'Strategic Insight'}
            </h4>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
            {isGenerating ? 'Synthesizing your transcript and vocal patterns...' : analysis || '"Complete your first session to see personalized tips here!"'}
          </p>
        </section>
      </main>

      {/* Sticky Bottom Actions */}
      <footer className="fixed bottom-0 left-0 right-0 p-6 bg-white/80 dark:bg-background-dark/80 backdrop-blur-xl border-t border-slate-200 dark:border-white/5 flex flex-col gap-3 z-50">
        <button
          onClick={onRestart}
          className="w-full bg-primary text-background-dark font-black h-16 rounded-2xl flex items-center justify-center gap-3 hover:opacity-90 transition-all shadow-xl shadow-primary/20 active:scale-95"
        >
          <RefreshCw className="size-5" />
          Prepare Again
        </button>
        <button
          onClick={handleDownloadPDF}
          className="w-full border border-slate-200 dark:border-slate-800 font-black h-14 rounded-2xl flex items-center justify-center gap-3 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all active:scale-95"
        >
          <Download className="size-5" />
          Download Full PDF Analysis
        </button>
      </footer>
    </div>
  );
}
