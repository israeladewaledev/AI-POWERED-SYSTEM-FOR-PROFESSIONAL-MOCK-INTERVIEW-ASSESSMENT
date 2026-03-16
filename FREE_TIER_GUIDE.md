# VocalAce Free-Tier & Local Integration Guide

This project has been updated to run **without paid API keys** (OpenAI). Here is how the new architecture works:

## 1. Local Speech-to-Text (Firdausi's Module)
Instead of OpenAI Whisper API, we use a local Python service running `faster-whisper`.

### Setup:
1. Open a new terminal.
2. Run the setup script: `bash setup_stt.sh`
3. Start the service: 
   ```bash
   source stt-service/venv/bin/activate
   python stt-service/main.py
   ```
4. The service will run on `http://localhost:8001`.

## 2. Intelligence Engine (Gemini 1.5 Flash)
We use Google's **Gemini 1.5 Flash**, which provides a massive free tier and ultra-low latency for developers. 

### Setup:
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Add it to your `.env.local` file:
   ```text
   GEMINI_API_KEY=your_key_here
   ```
3. The app is pre-configured to use the `gemini-1.5-flash` model.

## 3. Interviewer Voice (TTS)
We use the **Web Speech API** built into your browser. 
* **Cost**: $0.00
* **Benefit**: Zero latency and no setup required.

## 4. Acoustic Analysis (Maryam's Module)
This remains a custom local JavaScript implementation utilizing the browser's Web Audio API for maximum efficiency.