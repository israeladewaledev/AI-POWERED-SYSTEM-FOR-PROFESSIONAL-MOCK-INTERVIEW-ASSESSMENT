import { supabase } from '@/utils/supabase';

export interface TranscriptEntry {
  speaker: string;
  content: string;
  vocal_confidence?: number;
}

export const interviewService = {
  /**
   * Creates a new session record and returns the session ID.
   */
  async createSession(userId: string, jobTitle: string = 'General Practice') {
    try {
      const { data, error } = await supabase
        .from('sessions')
        .insert([{ user_id: userId, job_title: jobTitle, status: 'in-progress' }])
        .select()
        .single();

      if (error) {
        console.warn('Supabase Insert Error:', error);
        return 'mock-session-' + Date.now();
      }
      return data.id;
    } catch (err) {
      console.warn('Database connection failed, starting mock session:', err);
      return 'mock-session-' + Date.now();
    }
  },

  /**
   * Saves the final results of a session.
   */
  async finalizeSession(sessionId: string, overallScore: number, duration: number) {
    const { error } = await supabase
      .from('sessions')
      .update({
        overall_confidence_score: overallScore,
        duration_seconds: duration,
        status: 'completed'
      })
      .eq('id', sessionId);

    if (error) console.warn('Failed to finalize session in DB:', error);
  },

  /**
   * Logs a single turn of the transcript.
   */
  async logTranscriptItem(sessionId: string, entry: TranscriptEntry, order: number) {
    const { error } = await supabase
      .from('transcript_logs')
      .insert([{
        session_id: sessionId,
        speaker: entry.speaker,
        content: entry.content,
        vocal_confidence: entry.vocal_confidence,
        sequence_order: order
      }]);

    if (error) console.warn('Failed to log transcript item:', error);
  }
};
