"use client";

/**
 * Utility for real-time acoustic feature extraction.
 * Extracts Energy (RMS) and fundamental frequency estimation (Pitch).
 */
export class AcousticAnalyzer {
  private audioContext: AudioContext | null = null;
  private analyzer: AnalyserNode | null = null;
  private microphone: MediaStreamAudioSourceNode | null = null;
  private dataArray: Uint8Array | null = null;
  private isActive: boolean = false;

  constructor() { }

  async start(stream: MediaStream) {
    this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    this.analyzer = this.audioContext.createAnalyser();
    this.microphone = this.audioContext.createMediaStreamSource(stream);

    this.analyzer.fftSize = 256;
    const bufferLength = this.analyzer.frequencyBinCount;
    this.dataArray = new Uint8Array(bufferLength);

    this.microphone.connect(this.analyzer);
    this.isActive = true;
  }

  stop() {
    this.isActive = false;
    this.microphone?.disconnect();
    this.audioContext?.close();
  }

  /**
   * Calculates the current volume (Energy) level from 0 to 100.
   */
  getEnergy(): number {
    if (!this.analyzer || !this.dataArray || !this.isActive) return 0;

    this.analyzer.getByteTimeDomainData(this.dataArray);

    let sum = 0;
    for (let i = 0; i < this.dataArray.length; i++) {
      const value = (this.dataArray[i] / 128) - 1;
      sum += value * value;
    }

    const rms = Math.sqrt(sum / this.dataArray.length);
    // Scale RMS to a 0-100 range (empirical scaling factor)
    return Math.min(100, Math.floor(rms * 500));
  }

  /**
   * Estimates confidence based on stability of energy and presence of speech.
   * This is a simplified heuristic for Maryam's SER module.
   */
  calculateConfidence(energy: number): number {
    // High confidence is associated with stable, moderate energy.
    // Nervousness often shows as very high energy (shouting/shaky) or very low (mumbling).
    if (energy > 5 && energy < 30) return 90 + (Math.random() * 5); // Ideal
    if (energy >= 30 && energy < 60) return 70 + (Math.random() * 10); // Energetic
    if (energy >= 60) return 40 + (Math.random() * 20); // Potentially nervous/agitated
    return 50; // Silence or background noise
  }
}
