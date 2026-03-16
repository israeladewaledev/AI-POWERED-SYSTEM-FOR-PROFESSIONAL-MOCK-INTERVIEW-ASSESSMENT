"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import InterviewHeader from '@/components/InterviewHeader';
import VideoFeed from '@/components/VideoFeed';
import AnalysisSidebar from '@/components/AnalysisSidebar';
import RecordingControls from '@/components/RecordingControls';
import { useAudioRecorder } from '@/hooks/useAudioRecorder';
import { AcousticAnalyzer } from '@/utils/audioAnalysis';
import { interviewService } from '@/services/interviewService';
import { useInterview } from '@/context/InterviewContext';

export default function InterviewPage() {
  const router = useRouter();
  const {
    sessionId,
    questions,
    currentIdx,
    setCurrentIdx,
    transcript,
    setTranscript,
    confidence,
    setConfidence,
    confidenceHistory,
    setConfidenceHistory,
    resetInterview
  } = useInterview();

  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const analyzerRef = useRef<AcousticAnalyzer | null>(null);
  const confidenceIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);

  const { isRecording, audioBlob, startRecording, stopRecording, transcribeAudio } = useAudioRecorder();

  // Redirect if no session
  useEffect(() => {
    if (!sessionId && questions.length === 0) {
      router.push('/');
    } else if (questions.length > 0) {
      // Start first question if not started
      if (currentIdx === 0 && transcript.length === 1) {
        startTimeRef.current = Date.now();
        playQuestion(questions[0]);
      }
    }
  }, [sessionId, questions]);

  // Handle transcription when recording finishes
  useEffect(() => {
    if (audioBlob) {
      handleTranscription(audioBlob);
    }
  }, [audioBlob]);

  // Handle real-time confidence tracking (Maryam's Module)
  useEffect(() => {
    if (isRecording) {
      if (!analyzerRef.current) analyzerRef.current = new AcousticAnalyzer();
      navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        analyzerRef.current?.start(stream);
        confidenceIntervalRef.current = setInterval(() => {
          const energy = analyzerRef.current?.getEnergy() || 0;
          const score = analyzerRef.current?.calculateConfidence(energy) || 85;
          const roundedScore = Math.floor(score);
          setConfidence(roundedScore);
          setConfidenceHistory(prev => [...prev.slice(-49), roundedScore]); // Keep last 50 points
        }, 1000);
      });
    } else {
      analyzerRef.current?.stop();
      if (confidenceIntervalRef.current) clearInterval(confidenceIntervalRef.current);
    }
    return () => { if (confidenceIntervalRef.current) clearInterval(confidenceIntervalRef.current); };
  }, [isRecording]);

  const handleTranscription = async (blob: Blob) => {
    setIsProcessing(true);
    const text = await transcribeAudio(blob);
    if (text) {
      const entry = { speaker: 'Candidate', text };
      const updatedTranscript = [...transcript, entry];
      setTranscript(updatedTranscript);

      // Log to DB
      if (sessionId) {
        interviewService.logTranscriptItem(sessionId, {
          speaker: 'Candidate',
          content: text,
          vocal_confidence: confidence
        }, transcript.length);
      }

      // Decide: Next pre-set question OR follow-up?
      if (currentIdx < questions.length - 1) {
        setIsProcessing(true);
        try {
          // Generate follow-up contextually
          const res = await fetch('/api/interview/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              lastResponse: text,
              sessionTranscript: updatedTranscript
            })
          });
          const data = await res.json();
          const nextQuestion = data.data || questions[currentIdx + 1];

          const nextIdx = currentIdx + 1;
          setCurrentIdx(nextIdx);
          playQuestion(nextQuestion);
        } catch (err) {
          console.error("Follow-up generation failed", err);
          const nextIdx = currentIdx + 1;
          setCurrentIdx(nextIdx);
          playQuestion(questions[nextIdx]);
        }
      } else {
        handleStop();
      }
    }
    setIsProcessing(false);
  };

  const playQuestion = (text: string) => {
    setIsTTSPlaying(true);

    // Log interviewer turn
    if (sessionId) {
      interviewService.logTranscriptItem(sessionId, { speaker: 'Interviewer', content: text }, transcript.length);
    }

    // Using browser native Speech Synthesis
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onend = () => {
      setIsTTSPlaying(false);
      startRecording();
    };

    window.speechSynthesis.speak(utterance);
    setTranscript(prev => [...prev, { speaker: 'Interviewer', text }]);
  };

  const handleNext = () => {
    if (isRecording) stopRecording();
  };

  const handleStop = async () => {
    if (sessionId) {
      const duration = Math.floor((Date.now() - startTimeRef.current) / 1000);
      await interviewService.finalizeSession(sessionId, confidence, duration);
    }
    router.push('/report');
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else if (!isTTSPlaying && !isProcessing) {
      startRecording();
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-background-dark flex flex-col">
      <InterviewHeader />
      <main className="flex-1 flex flex-col lg:flex-row p-4 lg:p-6 gap-6 max-w-[1600px] mx-auto w-full mb-32">
        <div className="flex-1 min-h-[400px] lg:min-h-0 relative">
          <VideoFeed
            currentQuestion={questions[currentIdx] || "Preparing your questions..."}
            isRecording={isRecording}
          />
          <button
            onClick={handleNext}
            disabled={isProcessing || isTTSPlaying}
            className={`absolute bottom-6 right-6 z-30 px-8 py-4 rounded-2xl font-black uppercase tracking-widest shadow-2xl transition-all ${isProcessing || isTTSPlaying ? 'bg-slate-500 scale-95 opacity-50' : 'bg-primary text-background-dark hover:scale-105 active:scale-95'
              }`}
          >
            {isProcessing ? 'Transcribing...' : isTTSPlaying ? 'Interviewer Speaking...' : 'Submit Response'}
          </button>
        </div>
        <AnalysisSidebar
          confidence={confidence}
          transcript={transcript}
          isAnalyzing={isRecording || isTTSPlaying || isProcessing}
        />
      </main>
      <RecordingControls
        isRecording={isRecording}
        onStop={handleStop}
        onPause={toggleRecording} // Fixed: Link Play button to actual toggle
        onEdit={() => { }}
        onSave={() => { }}
        onShare={() => { }}
      />
    </div>
  );
}
