import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

export async function POST(req: NextRequest) {
  try {
    const { resumeText, lastResponse, sessionTranscript } = await req.json();

    let prompt = "";

    // Case 1: Initial Question Generation from Resume (STAR Method)
    if (resumeText && !lastResponse) {
      prompt = `
        You are a world-class technical recruiter at a FAANG company. 
        Analyze the following resume and identify 5 key achievements or technical claims.
        Generate 5 challenging interview questions using the STAR method (Situation, Task, Action, Result) 
        to probe the authenticity and depth of these claims.
        
        Resume Content:
        ${resumeText}
        
        Guidelines:
        - 2 questions should be strictly technical based on the mentioned stack.
        - 3 questions should be behavioral but tied to specific projects mentioned in the resume.
        - Ensure the tone is professional, rigorous, and observant.
        
        Return ONLY valid JSON.
        Format: {"questions": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]}
      `;
    }
    // Case 2: Deep Context-Aware Follow-up Question
    else if (lastResponse && sessionTranscript) {
      prompt = `
        You are conducting a rigorous technical interview. 
        The candidate just responded with: "${lastResponse}"
        
        Review the full conversation history:
        ${JSON.stringify(sessionTranscript)}
        
        Your Goal:
        1. Identify any vague parts of their answer (e.g., "we used cloud", "it was fast").
        2. Generate 1 sharp, analytical follow-up question that asks for specific metrics, 
           technical trade-offs, or the personal 'Action' they took in that scenario.
        
        Constraints:
        - NO generic questions like "Tell me more".
        - Be specific to the technology or project they just mentioned.
        - Return ONLY the question text as plain text. No markdown, no JSON.
      `;
    }
    else {
      return NextResponse.json({ error: 'Missing required context' }, { status: 400 });
    }

    const result = await model.generateContent(prompt);
    const text = result.response.text().trim();

    // Handle initial generation JSON parsing
    if (resumeText && !lastResponse) {
      try {
        // Find JSON start and end in case model includes markdown ticks
        const jsonStart = text.indexOf('{');
        const jsonEnd = text.lastIndexOf('}') + 1;
        const jsonStr = text.substring(jsonStart, jsonEnd);
        const parsedData = JSON.parse(jsonStr);
        return NextResponse.json({ data: parsedData });
      } catch (e) {
        console.error("JSON Parsing failed", text);
        return NextResponse.json({ data: { questions: ["Describe a complex technical problem you solved.", "How do you handle workplace conflict?", "Tell me about your background.", "What are your career goals?", "Why should we hire you?"] } });
      }
    }

    // Handle follow-up plain text
    return NextResponse.json({ data: text });
  } catch (error: any) {
    console.error('Question generation error:', error);
    return NextResponse.json({ error: 'Failed to generate questions. Check GEMINI_API_KEY.' }, { status: 500 });
  }
}
