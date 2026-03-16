"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import Dashboard from '@/components/Dashboard';
import { useInterview } from '@/context/InterviewContext';
import { interviewService } from '@/services/interviewService';

export default function Home() {
  const router = useRouter();
  const { setSessionId, setQuestions, setResumeText } = useInterview();

  const handleStartInterview = async (resumeText?: string) => {
    if (resumeText) setResumeText(resumeText);

    try {
      // 1. Generate Session (Mock User ID)
      const sid = await interviewService.createSession('00000000-0000-0000-0000-000000000000');
      setSessionId(sid);

      // 2. Generate AI Questions
      let generatedQuestions = ["Tell me about your background.", "Why are you interested in this role?", "Give an example of a time you faced a challenge."];

      try {
        const res = await fetch('/api/interview/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ resumeText })
        });
        const data = await res.json();
        if (data.data?.questions) {
          generatedQuestions = data.data.questions;
        }
      } catch (genErr) {
        console.warn('AI Question generation failed, using defaults:', genErr);
      }

      setQuestions(generatedQuestions);

      // 3. Navigate to interview
      router.push('/interview');
    } catch (err: any) {
      console.error('Final Initialization crash:', err.message || err);
      // Fallback redirect anyway so the app doesn't hang
      router.push('/interview');
    }
  };

  return <Dashboard onStartInterview={handleStartInterview} />;
}
