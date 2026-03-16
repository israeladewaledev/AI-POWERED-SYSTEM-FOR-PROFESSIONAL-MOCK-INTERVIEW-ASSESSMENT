#!/usr/bin/env python3
"""
Script to extract literature review information from PDF papers in Firdausi batch 3
Focus: Speech to Text
"""
import PyPDF2
import re
import os

def extract_full_text(pdf_file):
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return ''.join([page.extract_text() for page in reader.pages])
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return ""

def extract_info(pdf_file, text):
    """Extract structured information from paper text"""
    info = {
        'title': "Not explicitly stated",
        'authors': "Not explicitly stated",
        'year': "Not explicitly stated",
        'source': "Not explicitly stated",
        'abstract': "Not explicitly stated",
        'methodology': "Not explicitly stated",
        'technologies': "Not explicitly stated",
        'findings': "Not explicitly stated",
        'limitations': "Not explicitly stated"
    }
    
    # Extract title (first substantial line)
    lines = [l.strip() for l in text.split('\n')[:100] if len(l.strip()) > 10]
    if lines:
        info['title'] = lines[0][:200]
    
    # Extract year
    year_match = re.search(r'\b(20\d{2})\b', text[:3000])
    if year_match:
        info['year'] = year_match.group(1)
    
    # Extract authors
    author_patterns = [
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Author[:\s]+([^\n]+)',
        r'By\s+([^\n]+)',
        r'([A-Z]\.\s+[A-Z][a-z]+(?:\s+[A-Z]\.\s+[A-Z][a-z]+)*)'
    ]
    for pattern in author_patterns:
        match = re.search(pattern, text[:2000], re.IGNORECASE)
        if match and len(match.group(1)) > 5:
            info['authors'] = match.group(1).strip()
            break
    
    # Extract abstract
    abstract_patterns = [
        r'Abstract[:\s]*(.*?)(?:Keywords|Introduction|1\.|I\.|INTRODUCTION)',
        r'ABSTRACT[:\s]*(.*?)(?:Keywords|Introduction|1\.|I\.)',
    ]
    for pattern in abstract_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = match.group(1).strip()
            info['abstract'] = abstract[:1500]
            break
    
    # Extract source/journal
    source_patterns = [
        r'Journal\s+of\s+([^\n]{5,100})',
        r'Proceedings\s+of\s+([^\n]{5,100})',
        r'Conference\s+on\s+([^\n]{5,100})',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'Volume\s+[^\n]{0,50}',
    ]
    for pattern in source_patterns:
        match = re.search(pattern, text[:3000])
        if match:
            info['source'] = match.group(0).strip()[:200]
            break
    
    # Extract methodology keywords
    methodology_keywords = ['ASR', 'automatic speech recognition', 'CNN', 'LSTM', 'deep learning', 
                          'machine learning', 'neural network', 'NLP', 'transcription', 
                          'signal processing', 'qualitative', 'quantitative', 'experimental', 
                          'case study', 'transformer', 'attention mechanism']
    found_methods = [kw for kw in methodology_keywords if kw.lower() in text.lower()[:5000]]
    if found_methods:
        info['methodology'] = ", ".join(found_methods[:5])
    
    # Extract technologies
    tech_keywords = ['Python', 'TensorFlow', 'PyTorch', 'Librosa', 'Pydub', 'OpenCV',
                    'CNN', 'LSTM', 'RNN', 'NLP', 'MFCC', 'speech recognition', 'ASR',
                    'Whisper', 'Wav2Vec', 'Transformer', 'Google Speech API', 'Sphinx']
    found_tech = [kw for kw in tech_keywords if kw in text[:5000]]
    if found_tech:
        info['technologies'] = ", ".join(found_tech[:8])
    
    return info

def create_markdown(pdf_file, info):
    """Create markdown extraction file"""
    base_name = os.path.splitext(pdf_file)[0]
    output_file = f"{base_name}-Literature-Review-Extraction.md"
    
    # Determine relevance based on content - FOCUS ON SPEECH TO TEXT
    text_lower = info['abstract'].lower() + info['title'].lower()
    relevance = ""
    aspects = []
    
    if any(term in text_lower for term in ['speech recognition', 'asr', 'automatic speech', 'speech to text', 'transcription']):
        relevance += "This paper is highly relevant to the Firdausi component (speech to text) as it focuses on automatic speech recognition, speech transcription, or speech-to-text conversion. "
        aspects.append("Speech-to-Text Analysis")
        aspects.append("Methodology Justification")
    
    if any(term in text_lower for term in ['pronunciation', 'accent', 'language learning', 'efl', 'esl']):
        relevance += "The paper addresses pronunciation assessment or language learning applications of speech recognition, which supports speech-to-text functionality in educational or interview contexts. "
        aspects.append("System Design")
    
    if any(term in text_lower for term in ['interview', 'recruitment', 'candidate', 'hiring', 'oral']):
        relevance += "The study directly relates to interview systems, oral assessment, or candidate evaluation, providing direct support for the interview practice platform. "
        aspects.append("Problem Background")
        aspects.append("System Design")
    
    if any(term in text_lower for term in ['speech', 'voice', 'audio', 'vocal', 'utterance']):
        relevance += "The research involves speech or voice processing, which is fundamental to speech-to-text conversion. "
        if "Speech-to-Text Analysis" not in aspects:
            aspects.append("Speech-to-Text Analysis")
    
    if any(term in text_lower for term in ['accuracy', 'error rate', 'wer', 'cer', 'transcription quality']):
        relevance += "The study addresses accuracy metrics or transcription quality, which are critical for reliable speech-to-text systems. "
        aspects.append("Methodology Justification")
    
    if not relevance:
        relevance = "The paper may provide general insights into speech processing, AI systems, automatic transcription, or human-computer interaction that could inform the speech-to-text component design."
        aspects = ["System Design"]
    
    if not aspects:
        aspects = ["System Design"]
    
    md_content = f"""# Literature Review Extraction

## Paper: {info['title']}

---

### 1. Full Title of the Paper:
{info['title']}

### 2. Author(s) and Year of Publication:
{info['authors']} ({info['year']})

### 3. Source / Publisher:
{info['source']}

### 4. IEEE Reference Format:
Not explicitly stated (requires full citation details from paper)

### 5. Research Domain / Area:
Not explicitly stated (to be determined from full paper content)

### 6. Aim / Objective of the Study:
{info['abstract'][:500] if len(info['abstract']) > 100 else "Not explicitly stated"}

### 7. Methodology Used:
{info['methodology'] if info['methodology'] != "Not explicitly stated" else "Not explicitly stated"}

### 8. Technologies / Tools Mentioned (if any):
{info['technologies'] if info['technologies'] != "Not explicitly stated" else "Not explicitly stated"}

### 9. Key Findings / Contributions:
{info['findings'] if info['findings'] != "Not explicitly stated" else "Not explicitly stated"}

### 10. Identified Limitations (if stated):
{info['limitations']}

### 11. Relevance to the Current Project:
{relevance}

### 12. Aspect of the Project Supported:
{", ".join(aspects) if aspects else "System Design"}

---

*Extraction Date: [Current Date]*
*Extracted for: Chapter Two (Literature Review) - Final Year Project: "Design and Implementation of a web interview practice platform"*
*Component: Firdausi (Speech to Text)*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_file

# Process batch 3 papers (remaining papers)
batch3_files = [
    'fpsyg-13-902429.pdf',
    'FULLTEXT01 (1).pdf',
    'FULLTEXT01.pdf',
    'g2.pdf',
    'Humanoid robot as an educational assistant   insights of speech recognition for online and offline mode of teaching.pdf',
    'Integrating automatic speech recognition and automated writing evaluation to reduce speaking anxiety and enhance speaking competence among Chinese EFL.pdf',
    'Latifa_Vol+10+No+2_up.pdf',
    'Lee24.pdf',
    'MuhonenRiikka.pdf',
    'Paper+18.+Original.docx.pdf',
    'paper4.pdf',
    'qian-2025-automatic-speech-recognition-based-on-adaptive-parameters-technology-in-english-mooc-teaching-system.pdf',
    'Users-perceptions-of-ASR-as-a-writing-tool-an-analysis-using-the-technology-acceptance-model.pdf'
]

print("Processing Firdausi Batch 3 papers (Speech to Text focus)...")
for pdf_file in batch3_files:
    if os.path.exists(pdf_file):
        print(f"Processing {pdf_file}...")
        text = extract_full_text(pdf_file)
        if text:
            info = extract_info(pdf_file, text)
            output = create_markdown(pdf_file, info)
            print(f"  Created: {output}")
        else:
            print(f"  Failed to extract text from {pdf_file}")
    else:
        print(f"  File not found: {pdf_file}")

print("\nFirdausi Batch 3 processing complete!")

