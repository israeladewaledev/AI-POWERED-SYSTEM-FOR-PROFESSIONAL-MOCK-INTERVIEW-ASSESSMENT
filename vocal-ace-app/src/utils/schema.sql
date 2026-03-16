-- SQL Migration for VocalAce Platform

-- 1. Profiles Table (Extended User Data)
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  avatar_url TEXT,
  resume_text TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Sessions Table (Mock Interview Results)
CREATE TABLE IF NOT EXISTS public.sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  session_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  overall_confidence_score INTEGER,
  duration_seconds INTEGER,
  status TEXT DEFAULT 'completed',
  job_title TEXT
);

-- 3. Transcript Logs (Individual Responses & Analysis)
CREATE TABLE IF NOT EXISTS public.transcript_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID REFERENCES public.sessions(id) ON DELETE CASCADE,
  speaker TEXT NOT NULL, -- 'Interviewer' or 'Candidate'
  content TEXT NOT NULL,
  vocal_confidence INTEGER, -- Null for Interviewer
  audio_url TEXT, -- Link to storage if recording is kept
  sequence_order INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS (Row Level Security) - Basic setup
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcript_logs ENABLE ROW LEVEL SECURITY;

-- Simple policies (Owner only)
CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can view own sessions" ON public.sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view transcript for own sessions" ON public.transcript_logs FOR SELECT 
  USING (EXISTS (SELECT 1 FROM public.sessions WHERE id = transcript_logs.session_id AND user_id = auth.uid()));
