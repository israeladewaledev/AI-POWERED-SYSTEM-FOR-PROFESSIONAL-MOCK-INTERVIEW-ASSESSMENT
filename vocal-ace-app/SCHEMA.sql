-- 1. Create Sessions Table
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  job_title TEXT DEFAULT 'General Practice',
  overall_confidence_score INTEGER,
  duration_seconds INTEGER,
  status TEXT DEFAULT 'in-progress',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Create Transcript Logs Table
CREATE TABLE transcript_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  speaker TEXT NOT NULL, -- 'Candidate' or 'Interviewer'
  content TEXT NOT NULL,
  vocal_confidence INTEGER,
  sequence_order INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Enable RLS (Optional/Basic)
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE transcript_logs ENABLE ROW LEVEL SECURITY;

-- Allow anonymous inserts for demo purposes (NOT FOR PRODUCTION)
CREATE POLICY "Allow anon insert" ON sessions FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon select" ON sessions FOR SELECT USING (true);
CREATE POLICY "Allow anon update" ON sessions FOR UPDATE USING (true);

CREATE POLICY "Allow anon insert transcript" ON transcript_logs FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon select transcript" ON transcript_logs FOR SELECT USING (true);
