"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import PerformanceReport from '@/components/PerformanceReport';
import { useInterview } from '@/context/InterviewContext';

export default function ReportPage() {
  const router = useRouter();
  const { resetInterview } = useInterview();

  const handleRestart = () => {
    resetInterview();
    router.push('/');
  };

  return <PerformanceReport onRestart={handleRestart} />;
}
