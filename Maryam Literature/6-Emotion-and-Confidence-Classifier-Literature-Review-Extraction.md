# Literature Review Extraction

## Paper: Emotion and Confidence Classifier for Mock Interviews Using Artificial Intelligence

---

### 1. Full Title of the Paper:
Emotion and Confidence Classifier for Mock Interviews Using Artificial Intelligence

### 2. Author(s) and Year of Publication:
Shalini Bhaskar Bajaj (2025)

### 3. Source / Publisher:
International Journal of Innovative Research in Computer Science and Technology (IJIRCST), Volume 13, Issue 5, September 2025, Pages 38-43. Published by Innovative Research Publication. ISSN (Online): 2347-5552. DOI: https://doi.org/10.55524/ijircst.2025.13.5.6. Article ID: IRP-1682.

### 4. IEEE Reference Format:
S. B. Bajaj, "Emotion and confidence classifier for mock interviews using artificial intelligence," *International Journal of Innovative Research in Computer Science and Technology (IJIRCST)*, vol. 13, no. 5, pp. 38-43, Sep. 2025, doi: 10.55524/ijircst.2025.13.5.6.

### 5. Research Domain / Area:
Artificial Intelligence in Recruitment and Interview Assessment, Emotion Recognition Systems, Speech Analysis and Confidence Assessment, AI-Powered Mock Interview Platforms, Multimodal Human-Computer Interaction

### 6. Aim / Objective of the Study:
The study aims to develop an AI-powered simulation system for practicing interviews that narrows the preparation-performance gap. The system measures candidate performance in two critical areas: emotion (empathy) and confidence. The objective is to help candidates overcome stressful pre-interview situations, improve their self-perception and self-efficacy, and prepare them for real-life interviews by providing objective, data-driven feedback through automated analysis of facial expressions and vocal characteristics.

### 7. Methodology Used:
Experimental system design with multimodal input analysis. The methodology comprises several interconnected stages: (1) Data Acquisition - real-time audio-visual recording using webcam and microphone interfaces; (2) Emotion Analysis - using Convolutional Neural Networks (CNN) trained on facial expression datasets to classify seven basic emotions (fear, anger, sadness, happiness, surprise, disgust, neutral); (3) Speech Analysis - employing Natural Language Processing (NLP) to analyze pronunciation clarity, speech rate, use of filler words, verbal fluency, and coherence; (4) Confidence Assessment - examining prosodic characteristics including pitch variability, voice volume, and rate of hesitations using Pydub library for audio segmentation; (5) Knowledge Base Assessment - evaluating semantic correctness, syntax correctness, and answer correctness using NLP models; (6) Scoring Framework - weighted combination of emotion score (20%), speech score (20%), confidence score (10%), and knowledge score (50%).

### 8. Technologies / Tools Mentioned (if any):
- **Deep Learning Frameworks**: Convolutional Neural Networks (CNN), Long Short-Term Memory (LSTM), Recurrent Neural Networks (RNN)
- **Natural Language Processing (NLP)**: For speech recognition, semantic analysis, syntactic analysis, and content assessment
- **Audio Processing Libraries**: Pydub (for audio segmentation and preprocessing), Librosa (mentioned in literature review for feature extraction)
- **Datasets**: FER-2013, CK+, JAFFE (for training emotion recognition models)
- **Evaluation Metrics**: Recall, precision, F1-score
- **Activation Functions**: ReLU (Rectified Linear Unit), Softmax
- **Hardware Interfaces**: Webcam, microphone

### 9. Key Findings / Contributions:
The research demonstrates that an AI-based system can effectively analyze emotional states and confidence levels through multimodal input (video, audio, and textual data). The CNN-based emotion analysis mechanism achieved high success in classifying seven different emotions, with the model detecting positive emotions more efficiently than negative emotions. The confidence assessment mechanism successfully identified markers of confidence levels such as pitch variability, volume consistency, and speech rate. The study found strong associations between emotional states and confidence levels: positive emotions (joy and love) were consistently associated with increased confidence, while negative emotions (sadness and fear) were associated with decreased confidence. The system provides a comprehensive, objective, and actionable assessment framework that improves interview preparation by offering standardized, data-driven feedback. The weighted scoring system (emotion 20%, speech 20%, confidence 10%, knowledge 50%) reflects real-world significance of each dimension in interview performance.

### 10. Identified Limitations (if stated):
Not explicitly stated in the paper. However, the paper acknowledges challenges in existing systems such as time consumption, requirement for manual data entry, and challenges when assessing behaviour across various people, which the proposed system aims to address.

### 11. Relevance to the Current Project:
This paper is highly relevant to the Maryam component (speech to tone) of the web interview practice platform. The study directly addresses emotion and confidence analysis from speech and facial expressions, which aligns with the speech-to-tone conversion objective. The paper demonstrates the application of prosodic feature analysis (pitch variability, voice volume, speech rate) for confidence assessment, which is fundamental to tone analysis. The use of NLP and LSTM models for speech processing and recognition provides methodological guidance for implementing speech-to-tone conversion. The multimodal approach combining audio and visual analysis supports the comprehensive evaluation needed in an interview practice platform. The weighted scoring framework and objective assessment methodology can inform the design of feedback mechanisms in the Maryam system.

### 12. Aspect of the Project Supported:
- **System Design**: Provides architectural guidance for emotion and confidence analysis modules
- **Methodology Justification**: Demonstrates the effectiveness of CNN for emotion recognition and NLP/LSTM for speech analysis
- **Problem Background**: Establishes the need for AI-powered interview practice systems and the gap in existing solutions
- **Speech-to-Tone Analysis**: Directly supports the core functionality of Maryam through prosodic feature analysis and confidence assessment techniques

---

*Extraction Date: [Current Date]*
*Extracted for: Chapter Two (Literature Review) - Final Year Project: "Design and Implementation of a web interview practice platform"*

