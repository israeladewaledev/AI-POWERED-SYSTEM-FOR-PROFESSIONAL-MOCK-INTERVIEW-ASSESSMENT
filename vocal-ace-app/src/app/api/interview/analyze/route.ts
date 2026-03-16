import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

export async function POST(req: NextRequest) {
  try {
    const { transcript, confidenceHistory } = await req.json();

    if (!transcript || transcript.length === 0) {
      return NextResponse.json({ error: 'No transcript provided' }, { status: 400 });
    }

    const prompt = `
      You are a senior career coach and vocal performance expert. 
      Analyze the following mock interview session and provide a "Strategic Insight" for the candidate.
      
      Transcript:
      ${JSON.stringify(transcript)}
      
      Confidence History (second-by-second scores):
      ${JSON.stringify(confidenceHistory)}
      
      Your Goal:
      1. Briefly comment on the candidate's communication clarity and content.
      2. Mention how their "vocal confidence" (from the history) changed during specific parts of the interview.
      3. Provide 1-2 actionable tips for improvement.
      
      Tone: Professional, supportive, and data-driven.
      Length: 2-3 concise paragraphs.
      
      Return ONLY the plain text feedback. No markdown, no JSON headings.
    `;

    const result = await model.generateContent(prompt);
    const feedback = result.response.text().trim();

    return NextResponse.json({ feedback });
  } catch (error: any) {
    console.error('Analysis generation error:', error);
    return NextResponse.json({ error: 'Failed to generate analysis.' }, { status: 500 });
  }
}
