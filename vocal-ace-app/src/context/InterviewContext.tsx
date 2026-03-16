"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface TranscriptItem {
  speaker: string;
  text: string;
}

interface InterviewContextType {
  sessionId: string | null;
  setSessionId: (id: string | null) => void;
  questions: string[];
  setQuestions: (qs: string[]) => void;
  currentIdx: number;
  setCurrentIdx: (idx: number) => void;
  transcript: TranscriptItem[];
  setTranscript: React.Dispatch<React.SetStateAction<TranscriptItem[]>>;
  confidence: number;
  setConfidence: (val: number) => void;
  confidenceHistory: number[];
  setConfidenceHistory: React.Dispatch<React.SetStateAction<number[]>>;
  analysis: string;
  setAnalysis: (text: string) => void;
  resumeText: string;
  setResumeText: (text: string) => void;
  resetInterview: () => void;
}

const InterviewContext = createContext<InterviewContextType | undefined>(undefined);

export function InterviewProvider({ children }: { children: ReactNode }) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<string[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [transcript, setTranscript] = useState<TranscriptItem[]>([
    { speaker: 'Interviewer', text: 'Welcome! I have reviewed your profile. Ready to begin?' }
  ]);
  const [confidence, setConfidence] = useState(85);
  const [confidenceHistory, setConfidenceHistory] = useState<number[]>([]);
  const [analysis, setAnalysis] = useState('');
  const [resumeText, setResumeText] = useState('');

  // Persist session
  useEffect(() => {
    const savedId = localStorage.getItem('vocalace_session_id');
    const savedTranscript = localStorage.getItem('vocalace_transcript');
    const savedQuestions = localStorage.getItem('vocalace_questions');
    const savedHistory = localStorage.getItem('vocalace_confidence_history');
    const savedAnalysis = localStorage.getItem('vocalace_analysis');
    if (savedId) setSessionId(savedId);
    if (savedTranscript) try { setTranscript(JSON.parse(savedTranscript)); } catch (e) { }
    if (savedQuestions) try { setQuestions(JSON.parse(savedQuestions)); } catch (e) { }
    if (savedHistory) try { setConfidenceHistory(JSON.parse(savedHistory)); } catch (e) { }
    if (savedAnalysis) setAnalysis(savedAnalysis);
  }, []);

  useEffect(() => {
    if (sessionId) localStorage.setItem('vocalace_session_id', sessionId);
    else localStorage.removeItem('vocalace_session_id');
  }, [sessionId]);

  useEffect(() => {
    localStorage.setItem('vocalace_transcript', JSON.stringify(transcript));
  }, [transcript]);

  useEffect(() => {
    localStorage.setItem('vocalace_questions', JSON.stringify(questions));
  }, [questions]);

  useEffect(() => {
    localStorage.setItem('vocalace_confidence_history', JSON.stringify(confidenceHistory));
  }, [confidenceHistory]);

  useEffect(() => {
    localStorage.setItem('vocalace_analysis', analysis);
  }, [analysis]);

  const resetInterview = () => {
    setSessionId(null);
    setQuestions([]);
    setCurrentIdx(0);
    setTranscript([{ speaker: 'Interviewer', text: 'Welcome! I have reviewed your profile. Ready to begin?' }]);
    setConfidence(85);
    setConfidenceHistory([]);
    setAnalysis('');
    localStorage.removeItem('vocalace_session_id');
    localStorage.removeItem('vocalace_transcript');
    localStorage.removeItem('vocalace_questions');
    localStorage.removeItem('vocalace_confidence_history');
    localStorage.removeItem('vocalace_analysis');
  };

  return (
    <InterviewContext.Provider value={{
      sessionId, setSessionId,
      questions, setQuestions,
      currentIdx, setCurrentIdx,
      transcript, setTranscript,
      confidence, setConfidence,
      confidenceHistory, setConfidenceHistory,
      analysis, setAnalysis,
      resumeText, setResumeText,
      resetInterview
    }}>
      {children}
    </InterviewContext.Provider>
  );
}

export function useInterview() {
  const context = useContext(InterviewContext);
  if (context === undefined) {
    throw new Error('useInterview must be used within an InterviewProvider');
  }
  return context;
}
