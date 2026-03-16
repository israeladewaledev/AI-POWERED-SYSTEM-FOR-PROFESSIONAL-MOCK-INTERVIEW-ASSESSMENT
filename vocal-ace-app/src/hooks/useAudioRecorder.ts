"use client";

import { useState, useRef, useCallback } from 'react';

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        const fullBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(fullBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  const transcribeAudio = useCallback(async (blob: Blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'audio.webm');

    try {
      const res = await fetch('/api/interview/stt', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      return data.text as string;
    } catch (err) {
      console.error('Transcription failed', err);
      return null;
    }
  }, []);

  return {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
    transcribeAudio
  };
};
