#!/usr/bin/env python3
"""
Script to extract literature review information from PDF papers in batch 2
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
    methodology_keywords = ['CNN', 'LSTM', 'deep learning', 'machine learning', 'neural network', 
                          'NLP', 'prosodic', 'signal processing', 'qualitative', 'quantitative',
                          'experimental', 'case study']
    found_methods = [kw for kw in methodology_keywords if kw.lower() in text.lower()[:5000]]
    if found_methods:
        info['methodology'] = ", ".join(found_methods[:5])
    
    # Extract technologies
    tech_keywords = ['Python', 'TensorFlow', 'PyTorch', 'Librosa', 'Pydub', 'OpenCV',
                    'CNN', 'LSTM', 'RNN', 'NLP', 'MFCC', 'speech recognition']
    found_tech = [kw for kw in tech_keywords if kw in text[:5000]]
    if found_tech:
        info['technologies'] = ", ".join(found_tech[:8])
    
    return info

def create_markdown(pdf_file, info):
    """Create markdown extraction file"""
    base_name = os.path.splitext(pdf_file)[0]
    output_file = f"{base_name}-Literature-Review-Extraction.md"
    
    # Determine relevance based on content
    text_lower = info['abstract'].lower() + info['title'].lower()
    relevance = ""
    aspects = []
    
    if any(term in text_lower for term in ['prosod', 'tone', 'pitch', 'intonation', 'rhythm']):
        relevance += "This paper is highly relevant to the Maryam component (speech to tone) as it focuses on prosodic analysis, tone, pitch, or intonation patterns. "
        aspects.append("Speech-to-Tone Analysis")
        aspects.append("Methodology Justification")
    
    if any(term in text_lower for term in ['emotion', 'sentiment', 'feeling']):
        relevance += "The paper addresses emotion recognition or sentiment analysis, which supports tone and emotional state assessment in interview contexts. "
        aspects.append("System Design")
    
    if any(term in text_lower for term in ['interview', 'recruitment', 'candidate', 'hiring']):
        relevance += "The study directly relates to interview systems or candidate assessment, providing direct support for the interview practice platform. "
        aspects.append("Problem Background")
        aspects.append("System Design")
    
    if any(term in text_lower for term in ['speech', 'voice', 'audio', 'vocal']):
        relevance += "The research involves speech or voice analysis, which is fundamental to speech-to-tone conversion. "
        if "Speech-to-Tone Analysis" not in aspects:
            aspects.append("Speech-to-Tone Analysis")
    
    if not relevance:
        relevance = "The paper may provide general insights into speech processing, AI systems, or human-computer interaction that could inform the project design."
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
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_file

# Process batch 2 papers
batch2_files = [
    '2409.14769v1.pdf',
    '2431706804 - Simon Boateng - Simon_Wahab_CS_Capstone_Report.pdf',
    '2511.14779v1.pdf',
    '3_1117YIJIE_GAO.pdf',
    '3395035.3425221.pdf',
    '3491102.3517687.pdf',
    '3555117.pdf',
    '3579543.pdf',
    '36154-661-29250-1-10-20250720.pdf',
    '9446.pdf'
]

print("Processing Batch 2 papers...")
for pdf_file in batch2_files:
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

print("\nBatch 2 processing complete!")

