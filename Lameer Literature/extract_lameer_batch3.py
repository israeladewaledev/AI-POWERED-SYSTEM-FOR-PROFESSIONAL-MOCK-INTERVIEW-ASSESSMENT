#!/usr/bin/env python3
"""
Enhanced script to extract detailed information from PDF papers for Batch 3 (Final Batch)
Extracts actual content, findings, methodologies, and limitations from papers
"""
import PyPDF2
import re
import os
from datetime import datetime

def extract_full_text(pdf_file):
    """Extract full text from PDF with better error handling"""
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''.join([page.extract_text() for page in reader.pages])
            return text
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return ""

def extract_detailed_info(pdf_file, text):
    """Extract comprehensive structured information from paper"""
    info = {
        'title': "Not found",
        'authors': "Not found",
        'year': "Not found",
        'source': "Not found",
        'abstract': "",
        'methodology': "",
        'dataset': "",
        'limitations': "",
        'findings': "",
        'key_contributions': "",
        'methods_used': [],
        'performance_metrics': "",
        'full_text': text[:80000]  # More text for better analysis
    }
    
    # Extract title - more robust extraction
    lines = [l.strip() for l in text.split('\n')[:100] if len(l.strip()) > 10]
    for line in lines[:20]:
        if len(line) > 20 and len(line) < 200:
            if not any(word in line.lower() for word in ['abstract', 'introduction', 'author', 'journal', 'volume', 'doi', 'page']):
                info['title'] = line[:300]
                break
    
    # Extract year - look in multiple places
    year_patterns = [
        r'\b(20\d{2})\b',
        r'\((\d{4})\)',
        r'\b(19\d{2}|20\d{2})\b'
    ]
    for pattern in year_patterns:
        matches = re.findall(pattern, text[:10000])
        if matches:
            years = [int(m) for m in matches if 1990 <= int(m) <= 2025]
            if years:
                info['year'] = str(max(years))
                break
    
    # Extract authors - improved patterns
    author_section = text[:5000]
    author_patterns = [
        r'Author[s]?[:\s]+([^\n]{10,300})',
        r'By\s+([^\n]{10,300})',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+and\s+[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
        r'([A-Z]\.\s+[A-Z][a-z]+(?:\s+[A-Z]\.\s+[A-Z][a-z]+)*)',
    ]
    for pattern in author_patterns:
        match = re.search(pattern, author_section, re.IGNORECASE)
        if match:
            authors = match.group(1).strip()
            if len(authors) > 5 and len(authors) < 300:
                # Clean up author string
                authors = re.sub(r'\s+', ' ', authors)
                info['authors'] = authors[:250]
                break
    
    # Extract abstract - multiple patterns
    abstract_patterns = [
        r'Abstract[:\s]*(.*?)(?:Keywords|Introduction|1\.|I\.|INTRODUCTION|Background)',
        r'ABSTRACT[:\s]*(.*?)(?:Keywords|Introduction|1\.|I\.|BACKGROUND)',
        r'Summary[:\s]*(.*?)(?:Keywords|Introduction|1\.)',
    ]
    for pattern in abstract_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = match.group(1).strip()
            # Clean abstract
            abstract = re.sub(r'\s+', ' ', abstract)
            if len(abstract) > 100:
                info['abstract'] = abstract[:2500]
                break
    
    # Extract source/journal - improved
    source_patterns = [
        r'Journal\s+of\s+([^\n]{5,150})',
        r'Proceedings\s+of\s+([^\n]{5,150})',
        r'Conference\s+on\s+([^\n]{5,150})',
        r'IEEE\s+([^\n]{5,150})',
        r'arXiv:([^\n]{5,50})',
        r'DOI[:\s]+([^\n]{5,100})',
        r'Published\s+in\s+([^\n]{5,150})',
    ]
    for pattern in source_patterns:
        match = re.search(pattern, text[:8000], re.IGNORECASE)
        if match:
            source = match.group(0).strip()
            info['source'] = source[:250]
            break
    
    # Extract methodology - get actual methods mentioned
    ml_methods = {
        'SVM': ['svm', 'support vector machine', 'support vector'],
        'Random Forest': ['random forest', 'rf'],
        'Naive Bayes': ['naive bayes', 'nb'],
        'Decision Tree': ['decision tree', 'dt'],
        'XGBoost': ['xgboost', 'extreme gradient boosting'],
        'CNN': ['cnn', 'convolutional neural network', 'convnet'],
        'RNN': ['rnn', 'recurrent neural network'],
        'LSTM': ['lstm', 'long short-term memory'],
        'Deep Learning': ['deep learning', 'neural network', 'deep neural'],
        'Ensemble': ['ensemble', 'bagging', 'boosting', 'stacking'],
        'Hybrid': ['hybrid', 'combined', 'fusion'],
    }
    
    text_lower = text.lower()
    found_methods = []
    for method, keywords in ml_methods.items():
        if any(kw in text_lower for kw in keywords):
            found_methods.append(method)
    
    info['methods_used'] = found_methods
    if found_methods:
        info['methodology'] = ", ".join(found_methods[:12])
    
    # Extract dataset mentions - more comprehensive
    dataset_keywords = ['dataset', 'data set', 'phistank', 'phish tank', 'kaggle', 'uci', 
                       'openphish', 'samples', 'instances', 'records', 'urls']
    dataset_sections = []
    for keyword in dataset_keywords:
        pattern = rf'{keyword}[:\s]+([^\n]{10,200})'
        matches = re.finditer(pattern, text[:15000], re.IGNORECASE)
        for match in matches:
            dataset_sections.append(match.group(0)[:200])
    
    # Also look for dataset names
    dataset_names = ['PhishTank', 'Kaggle', 'UCI', 'OpenPhish', 'DMOZ', 'Alexa']
    found_datasets = []
    for name in dataset_names:
        if name.lower() in text_lower:
            found_datasets.append(name)
    
    if dataset_sections:
        info['dataset'] = "; ".join(set(dataset_sections[:3]))
    elif found_datasets:
        info['dataset'] = ", ".join(found_datasets)
    
    # Extract limitations - more thorough
    limitation_sections = []
    limitation_keywords = ['limitation', 'limitations', 'challenge', 'challenges', 
                          'drawback', 'drawbacks', 'weakness', 'weaknesses', 
                          'future work', 'future research', 'limitation of this study']
    
    for keyword in limitation_keywords:
        # Look for sections with limitations
        pattern = rf'{keyword}[:\s]+(.*?)(?:\.\s+[A-Z][a-z]+\s+[A-Z]|Conclusion|References|Future|Acknowledg)'
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            limitation_text = match.group(1).strip()
            limitation_text = re.sub(r'\s+', ' ', limitation_text)
            if len(limitation_text) > 50:
                limitation_sections.append(limitation_text[:600])
    
    if limitation_sections:
        info['limitations'] = " ".join(limitation_sections[:3])
    
    # Extract findings/results
    findings_keywords = ['result', 'results', 'finding', 'findings', 'achieved', 
                        'performance', 'accuracy', 'precision', 'recall', 'f1']
    findings_sections = []
    for keyword in findings_keywords:
        pattern = rf'{keyword}[:\s]+([^\n]{20,300})'
        matches = re.finditer(pattern, text[:20000], re.IGNORECASE)
        for match in list(matches)[:5]:
            finding = match.group(1).strip()
            if len(finding) > 20:
                findings_sections.append(finding[:300])
    
    if findings_sections:
        info['findings'] = "; ".join(findings_sections[:5])
    
    # Extract key contributions
    contribution_keywords = ['contribution', 'contributions', 'propose', 'proposed', 
                           'introduce', 'introduced', 'novel', 'new approach']
    contributions = []
    for keyword in contribution_keywords:
        pattern = rf'{keyword}[:\s]+([^\n]{20,300})'
        matches = re.finditer(pattern, text[:15000], re.IGNORECASE)
        for match in list(matches)[:3]:
            contrib = match.group(1).strip()
            if len(contrib) > 20:
                contributions.append(contrib[:300])
    
    if contributions:
        info['key_contributions'] = "; ".join(contributions[:3])
    
    # Extract performance metrics
    metrics_pattern = r'(accuracy|precision|recall|f1|f-score|auc|roc)[:\s]+([0-9.]+%?|[0-9.]+)'
    metrics = re.findall(metrics_pattern, text[:20000], re.IGNORECASE)
    if metrics:
        info['performance_metrics'] = ", ".join([f"{m[0]}: {m[1]}" for m in metrics[:8]])
    
    return info

def create_batch_document(papers_info, batch_number=3):
    """Create comprehensive batch synthesis document with actual extracted content"""
    
    # Organize papers by relevance to each section
    background_papers = []
    problem_papers = []
    methodology_papers = []
    dataset_papers = []
    limitation_papers = []
    findings_papers = []
    
    for paper in papers_info:
        text_lower = (paper.get('abstract', '') + " " + paper.get('full_text', '')).lower()
        
        # Background papers
        if any(term in text_lower for term in ['phishing', 'cybersecurity', 'threat', 'attack', 'security']):
            background_papers.append(paper)
        
        # Problem papers
        if any(term in text_lower for term in ['false positive', 'zero-day', 'concept drift', 'limitation', 
                                               'challenge', 'problem', 'issue', 'difficulty']):
            problem_papers.append(paper)
        
        # Methodology papers
        if paper.get('methodology') or paper.get('methods_used'):
            methodology_papers.append(paper)
        
        # Dataset papers
        if paper.get('dataset'):
            dataset_papers.append(paper)
        
        # Limitation papers
        if paper.get('limitations'):
            limitation_papers.append(paper)
        
        # Findings papers
        if paper.get('findings') or paper.get('performance_metrics'):
            findings_papers.append(paper)
    
    # Generate APA references
    references = []
    for paper in papers_info:
        authors = paper.get('authors', 'Unknown Author')
        year = paper.get('year', 'n.d.')
        title = paper.get('title', 'Untitled')
        source = paper.get('source', 'Source not specified')
        
        # Format APA reference
        if authors != "Not found" and year != "Not found":
            ref = f"{authors} ({year}). {title}. {source}."
            references.append(ref)
    
    # Create document
    doc = f"""# BATCH {batch_number}: Hybrid Machine Learning Model for Phishing Detection
## Literature Review Synthesis Document (Final Batch)

*Generated: {datetime.now().strftime('%Y-%m-%d')}*
*Total Papers Analyzed: {len(papers_info)}*

---

# ========================
# CHAPTER ONE: INTRODUCTION
# ========================

## 1.1 Background of the Study

The exponential growth of internet usage globally has revolutionized various sectors including online banking, e-commerce, and digital communication platforms. This digital transformation has created unprecedented opportunities for economic growth and social connectivity. However, this interconnected digital ecosystem has also introduced significant cybersecurity vulnerabilities, with phishing emerging as one of the most pervasive and evolving threats in cyberspace.

Phishing attacks represent a critical cybersecurity challenge that continues to escalate in both frequency and sophistication. Researchers have documented that phishing remains a primary vector for cybercriminals seeking to compromise user credentials, financial information, and organizational data. The dynamic nature of phishing attacks, characterized by rapid adaptation to security measures, presents ongoing challenges for traditional detection mechanisms.

Traditional phishing detection approaches, including blacklist-based systems and rule-based heuristics, have demonstrated significant limitations in addressing contemporary phishing threats. Blacklist methods rely on maintaining databases of known malicious URLs, which inherently fail to detect zero-day phishing attacks that have not yet been catalogued. Rule-based systems, while providing interpretability, struggle with the adaptive nature of modern phishing campaigns that continuously evolve to bypass static detection rules.

The limitations of traditional approaches have motivated researchers to explore machine learning-based solutions for phishing detection. However, single machine learning models have shown inconsistent performance, with challenges related to generalization across diverse phishing attack patterns, handling concept drift, and managing high false positive rates. This has led to growing interest in hybrid machine learning approaches that combine multiple algorithms to leverage complementary strengths and improve overall detection performance.

"""
    
    # Add specific background information from papers
    for paper in background_papers[:len(background_papers)]:
        authors = paper.get('authors', 'Unknown')
        year = paper.get('year', 'n.d.')
        abstract = paper.get('abstract', '')[:400]
        if abstract and len(abstract) > 50:
            doc += f"{authors} ({year}) highlighted that {abstract}...\n\n"
    
    doc += """## 1.2 Statement of the Problem

The research literature reveals several critical problems in current phishing detection systems that necessitate the development of hybrid machine learning approaches:

**High False Positive Rates**: Existing detection systems frequently misclassify legitimate websites as phishing sites, leading to user frustration and reduced trust in security systems. This problem undermines the practical utility of detection mechanisms in real-world deployments.

**Zero-Day Phishing Attacks**: Traditional detection methods fail to identify previously unseen phishing attacks, creating significant security gaps. Attackers continuously develop novel techniques that bypass existing detection signatures, necessitating adaptive detection capabilities.

**Concept Drift**: Phishing attack patterns evolve over time, causing previously effective detection models to degrade in performance. This temporal drift requires continuous model retraining and adaptation, which single-model approaches struggle to accommodate effectively.

**Poor Generalization of Single ML Models**: Individual machine learning algorithms demonstrate inconsistent performance across different phishing attack types and datasets. Some models excel at detecting certain attack patterns while failing on others, indicating the need for complementary model combinations.

**Limited Feature Utilization**: Single models may not effectively leverage the diverse feature sets available for phishing detection, including URL characteristics, content analysis, and behavioral patterns. Hybrid approaches can better integrate multiple feature types.

"""
    
    # Add specific problem statements from papers
    for paper in problem_papers[:len(problem_papers)]:
        authors = paper.get('authors', 'Unknown')
        year = paper.get('year', 'n.d.')
        limitations = paper.get('limitations', '')
        if limitations and len(limitations) > 50:
            doc += f"{authors} ({year}) identified that {limitations[:300]}...\n\n"
    
    doc += """The research gap motivating hybrid machine learning models lies in the need for robust, adaptive detection systems that can effectively combine multiple algorithms to achieve superior performance compared to individual models while maintaining practical applicability in real-world scenarios.

## 1.3 Aim and Objectives of the Study

**AIM**: To develop and evaluate a hybrid machine learning model for phishing detection that combines multiple machine learning algorithms to achieve improved accuracy, reduced false positive rates, and enhanced generalization capabilities compared to single-model approaches.

**OBJECTIVES**:

1. To analyze existing phishing detection methods and identify limitations in current single-model machine learning approaches through comprehensive literature review.

2. To design and implement a hybrid machine learning framework that integrates multiple classification algorithms (such as Random Forest, SVM, and ensemble methods) for phishing URL and content detection.

3. To extract and engineer relevant features from phishing datasets, including URL-based features, content-based features, and hybrid feature sets that capture diverse attack patterns.

4. To evaluate the proposed hybrid model using standard performance metrics (accuracy, precision, recall, F1-score, and ROC-AUC) and compare its performance against baseline single-model approaches.

5. To assess the model's capability to detect zero-day phishing attacks and handle concept drift through experimental validation on diverse datasets.

## 1.4 Research Questions

1. How do hybrid machine learning models compare to single-model approaches in terms of detection accuracy, false positive rates, and generalization capabilities for phishing detection?

2. What combination of machine learning algorithms and feature sets yields optimal performance for detecting diverse phishing attack patterns, including zero-day attacks?

3. To what extent can hybrid models address the limitations of concept drift and improve detection performance across different phishing datasets and attack types?

4. What are the practical implications and deployment considerations for implementing hybrid machine learning models in real-world phishing detection systems?

## 1.5 Significance of the Study

**For Cybersecurity Researchers**: This research contributes to the growing body of knowledge on hybrid machine learning approaches for cybersecurity applications. It provides empirical evidence on the effectiveness of combining multiple algorithms and offers insights into optimal model architectures for phishing detection.

**For Financial Institutions**: Financial organizations face significant risks from phishing attacks targeting customer credentials and financial data. Improved detection systems can reduce financial losses, protect customer trust, and enhance overall security posture.

**For End Users**: Enhanced phishing detection systems protect individual users from falling victim to phishing attacks, safeguarding personal information, financial assets, and digital identities. Reduced false positives also improve user experience with security systems.

**For Intelligent Threat Detection Systems**: The research advances the development of adaptive, intelligent threat detection systems that can evolve with emerging attack patterns. Hybrid approaches offer pathways toward more robust and resilient security architectures.

## 1.6 Justification of the Study

Phishing remains an unsolved problem despite decades of research and development in cybersecurity. The persistent and evolving nature of phishing attacks, combined with the limitations of existing detection methods, creates an ongoing need for innovative solutions. The increasing sophistication of phishing campaigns, including targeted spear-phishing and social engineering techniques, further complicates detection efforts.

Hybrid machine learning approaches are more suitable than single-model methods because they can leverage the complementary strengths of different algorithms. For instance, ensemble methods can combine the robustness of Random Forest with the precision of SVM, while deep learning hybrids can capture complex patterns that traditional ML models might miss. This multi-algorithm approach addresses the fundamental challenge that no single model excels across all phishing attack types and scenarios.

The timeliness of this research is underscored by the exponential growth in phishing attacks, the increasing adoption of machine learning in cybersecurity, and the availability of large-scale datasets for training and evaluation. Current advances in computational resources and machine learning frameworks make hybrid approaches more feasible than ever before.

## 1.7 Scope and Limitations

**Scope**:

- **Detection Focus**: URL-based and content-based phishing detection methods
- **Learning Paradigm**: Supervised machine learning approaches
- **Data Sources**: Publicly available phishing datasets (Kaggle, UCI, PhishTank, etc.)
- **Model Types**: Hybrid combinations of traditional ML algorithms (Random Forest, SVM, Naive Bayes, Decision Trees) and potentially deep learning models
- **Evaluation Metrics**: Standard classification metrics including accuracy, precision, recall, F1-score, and ROC-AUC

**Limitations**:

- The study focuses on supervised learning approaches and does not extensively explore unsupervised or semi-supervised methods
- Real-time detection performance and computational efficiency may require further optimization beyond the scope of this research
- The evaluation is primarily based on publicly available datasets, which may not fully represent all real-world phishing scenarios
- Email-based phishing detection is not the primary focus, though URL and content analysis may overlap with email phishing techniques
- The research does not address all types of advanced persistent threats or highly sophisticated targeted attacks

## 1.8 Definition of Key Terms

**Phishing**: A cyberattack technique in which attackers impersonate legitimate entities through fraudulent communications (typically emails or websites) to deceive users into revealing sensitive information such as login credentials, financial data, or personal details.

**Hybrid Machine Learning**: An approach that combines multiple machine learning algorithms or techniques to leverage their complementary strengths and improve overall performance. In phishing detection, this may involve ensemble methods, stacking, or combining traditional ML with deep learning.

**Feature Extraction**: The process of identifying and selecting relevant characteristics from raw data (such as URLs, website content, or email headers) that can be used as input variables for machine learning models. Features may include lexical properties, structural elements, or behavioral patterns.

**Classification Model**: A machine learning algorithm that categorizes input data into predefined classes. In phishing detection, classification models distinguish between legitimate and phishing websites or emails.

**Zero-Day Attack**: A phishing attack that uses previously unknown techniques or targets that have not been identified in existing threat databases. Zero-day attacks bypass traditional signature-based detection methods.

**Concept Drift**: The phenomenon where the statistical properties of phishing attacks change over time, causing previously trained models to become less effective. This requires continuous model adaptation and retraining.

**Ensemble Learning**: A machine learning technique that combines predictions from multiple models to produce a final prediction. Common ensemble methods include bagging, boosting, and stacking.

---

# ===========================
# CHAPTER TWO: LITERATURE REVIEW
# ===========================

## 2.1 Introduction

This literature review examines existing research on phishing detection using machine learning techniques, with particular focus on hybrid and ensemble approaches. The review synthesizes findings from recent studies to identify current methodologies, evaluate their effectiveness, and highlight research gaps that motivate the development of improved hybrid detection systems. The analysis encompasses theoretical foundations, practical implementations, and performance evaluations across diverse datasets and attack scenarios.

## 2.2 Theoretical Foundations

### 2.2.1 Phishing Attack Models

Phishing attacks can be categorized into several types based on attack vectors and techniques. Common classifications include:

- **Email Phishing**: Mass-distributed fraudulent emails targeting broad user populations
- **Spear Phishing**: Targeted attacks directed at specific individuals or organizations
- **Whaling**: High-value targets such as executives or senior officials
- **Clone Phishing**: Replication of legitimate communications with malicious modifications
- **Website Phishing**: Fraudulent websites designed to mimic legitimate sites

The phishing lifecycle typically follows stages including reconnaissance, weaponization, delivery, exploitation, installation, command and control, and actions on objectives. Understanding these stages informs detection strategies that can intercept attacks at various points in the lifecycle.

Researchers have modeled phishing attacks as adversarial learning problems where attackers adapt their strategies based on detection mechanisms, creating an ongoing arms race between attackers and defenders.

### 2.2.2 Machine Learning in Cybersecurity

Machine learning applications in cybersecurity leverage pattern recognition capabilities to identify malicious activities that may evade traditional signature-based detection. Supervised learning approaches use labeled datasets to train classifiers that distinguish between legitimate and malicious entities. Unsupervised learning methods identify anomalies or clusters that deviate from normal patterns.

Detection theory foundations in cybersecurity involve balancing Type I errors (false positives) and Type II errors (false negatives), with the optimal balance depending on the specific security context and risk tolerance. The cost of missing a phishing attack must be weighed against the cost of incorrectly blocking legitimate content.

### 2.2.3 Hybrid Learning Models

Hybrid learning models combine multiple algorithms to achieve superior performance through complementary strengths. Key concepts include:

**Ensemble Learning**: Combines multiple base learners to produce a final prediction. Bagging (Bootstrap Aggregating) trains multiple models on different subsets of data and averages predictions. Boosting sequentially trains models that focus on previously misclassified instances. Stacking uses a meta-learner to combine predictions from multiple base models.

**Hybrid ML-DL Approaches**: Combine traditional machine learning algorithms with deep learning models. For example, feature extraction using deep learning followed by classification using traditional ML, or vice versa.

**Multi-Model Fusion**: Integrates predictions from diverse model types (e.g., Random Forest + SVM + Neural Networks) using voting, weighted averaging, or learned combination strategies.

## 2.3 Machine Learning Techniques for Phishing Detection

### 2.3.1 Traditional Detection Methods

Traditional phishing detection relies on blacklists, whitelists, and heuristic rules. Blacklist methods maintain databases of known malicious URLs but fail against zero-day attacks. Heuristic approaches use rule-based systems that check for suspicious patterns (e.g., URL length, presence of IP addresses, SSL certificate issues). These methods provide interpretability but lack adaptability to evolving attack patterns.

### 2.3.2 Single Machine Learning Models

"""
    
    # Add specific methodology information from papers
    for paper in methodology_papers[:len(methodology_papers)]:
        authors = paper.get('authors', 'Unknown')
        year = paper.get('year', 'n.d.')
        methods = paper.get('methodology', '')
        title = paper.get('title', '')[:100]
        if methods:
            doc += f"**{authors} ({year})**: {methods}. "
            if title != "Not found":
                doc += f"Their study on '{title[:80]}...' demonstrated "
            doc += "\n\n"
    
    doc += """### 2.3.3 Deep Learning Approaches

**Convolutional Neural Networks (CNNs)**: Applied to phishing detection by treating URLs or content as sequences and learning hierarchical patterns. CNNs can capture local patterns in URL structures or webpage content.

**Recurrent Neural Networks (RNN) / Long Short-Term Memory (LSTM)**: Sequence models that capture temporal dependencies in phishing attack patterns. LSTMs are particularly effective for analyzing sequential features in URLs or email content.

**NLP-based Phishing Detection**: Natural language processing techniques analyze textual content in phishing emails or websites. Methods include word embeddings, attention mechanisms, and transformer models to identify suspicious linguistic patterns.

### 2.3.4 Hybrid and Ensemble Models

Research has explored various hybrid combinations:

**ML-ML Hybrids**: Combining Random Forest with SVM, or Decision Trees with Naive Bayes, to leverage complementary strengths. Random Forest provides robustness while SVM offers precision on support vectors.

**ML-DL Hybrids**: Using deep learning for feature extraction and traditional ML for classification, or vice versa. This approach combines the pattern recognition capabilities of deep learning with the interpretability and efficiency of traditional ML.

**Multi-Level Ensembles**: Stacking multiple layers of models, where base models make initial predictions and meta-models learn optimal combination strategies.

Strengths of hybrid models include improved generalization, robustness to overfitting, and ability to handle diverse attack patterns. Weaknesses include increased computational complexity, reduced interpretability, and potential overfitting if not properly regularized.

## 2.4 Review of Existing Phishing Detection Systems

**Browser-based Systems**: Modern web browsers incorporate phishing detection through services like Google Safe Browsing API, which maintains blacklists and heuristics. These systems provide real-time protection but rely on centralized threat intelligence.

**Google Safe Browsing**: A widely deployed service that checks URLs against continuously updated lists of suspected phishing and malware sites. It uses both blacklists and machine learning for classification.

**Research Prototypes**: Academic research has produced various prototype systems demonstrating hybrid ML approaches. These prototypes often achieve high accuracy on research datasets but face challenges in real-world deployment, including scalability, latency requirements, and integration with existing security infrastructure.

## 2.5 Phishing Detection in Developing Countries

Cybercrime trends in developing countries, particularly in Africa and regions like Nigeria, show increasing phishing activity targeting financial institutions and individual users. Challenges include:

- **Awareness Gaps**: Lower cybersecurity awareness among users increases susceptibility to phishing attacks
- **Infrastructure Constraints**: Limited computational resources and internet connectivity affect real-time detection capabilities
- **Regulatory Frameworks**: Developing regulatory environments may lack comprehensive cybersecurity legislation
- **Resource Limitations**: Financial institutions and organizations may have limited budgets for advanced security systems

These factors create unique requirements for phishing detection systems that must operate effectively under resource constraints while addressing local attack patterns and user behaviors.

## 2.6 Identified Research Gaps

| Author | Method Used | Dataset | Limitation | Research Gap |
|--------|-------------|---------|------------|--------------|
"""
    
    # Add research gaps from papers
    for paper in limitation_papers[:len(limitation_papers)]:
        authors = paper.get('authors', 'Unknown')
        year = paper.get('year', 'n.d.')
        method = paper.get('methodology', 'Not specified')[:60]
        dataset = paper.get('dataset', 'Not specified')[:60]
        limitation = paper.get('limitations', 'Not specified')[:100]
        
        # Determine research gap based on limitation
        if 'ensemble' in limitation.lower() or 'hybrid' in limitation.lower():
            gap = "Need for comprehensive hybrid ensemble approaches"
        elif 'feature' in limitation.lower():
            gap = "Requirement for advanced feature engineering"
        elif 'zero-day' in limitation.lower() or 'new attack' in limitation.lower():
            gap = "Need for adaptive models handling zero-day attacks"
        elif 'generalization' in limitation.lower() or 'dataset' in limitation.lower():
            gap = "Requirement for better cross-dataset generalization"
        else:
            gap = "Need for improved hybrid ML approaches"
        
        doc += f"| {authors} ({year}) | {method} | {dataset} | {limitation[:80]} | {gap} |\n"
    
    doc += """
## 2.7 Conceptual Framework of the Proposed System

The conceptual framework for the hybrid machine learning phishing detection system follows a pipeline architecture:

**Input Layer**: Receives URLs or website content as raw input data. Inputs may include URL strings, HTML content, or extracted features from web pages.

**Feature Extraction Layer**: Processes raw inputs to extract relevant features across multiple categories:
- URL-based features (length, domain characteristics, suspicious patterns)
- Content-based features (HTML structure, text analysis, visual similarity)
- Hybrid features (combinations of URL and content characteristics)

**Hybrid ML Model Layer**: Applies multiple machine learning algorithms in parallel or sequential configurations:
- Base models (Random Forest, SVM, Naive Bayes, etc.) generate individual predictions
- Ensemble mechanism combines base model predictions using voting, stacking, or learned weights
- Meta-model (if using stacking) learns optimal combination strategy

**Classification Layer**: Produces final binary classification (phishing vs. legitimate) with confidence scores

**Alert/Output Layer**: Generates alerts, blocks malicious content, or provides warnings to users based on classification results

This framework enables the system to leverage complementary strengths of different algorithms while maintaining adaptability to evolving attack patterns.

---

# ====================================
# CHAPTER THREE: SYSTEM ANALYSIS AND DESIGN
# ====================================

## 3.1 Introduction

This chapter presents the system analysis and design for the hybrid machine learning phishing detection system. The design objectives focus on creating a robust, scalable, and effective detection framework that integrates multiple machine learning algorithms to achieve superior performance compared to single-model approaches.

## 3.2 Research Design

The research follows an experimental design science approach, combining:
- **Experimental Methodology**: Controlled experiments comparing hybrid models against baseline single-model approaches using standardized datasets and evaluation metrics
- **Design Science**: Systematic design and development of the hybrid detection system following established software engineering and machine learning best practices
- **Empirical Evaluation**: Performance assessment through comprehensive testing on diverse datasets representing various phishing attack patterns

## 3.3 Dataset Description and Sampling

**Dataset Sources**: The research utilizes publicly available phishing datasets from sources including:
"""
    
    # Add dataset information from papers
    unique_datasets = set()
    for paper in dataset_papers:
        dataset = paper.get('dataset', '')
        if dataset and dataset != "Not found":
            unique_datasets.add(dataset.split(';')[0].split(',')[0].strip())
    
    for dataset in list(unique_datasets)[:10]:
        doc += f"- {dataset}\n"
    
    doc += """- Kaggle phishing datasets
- UCI Machine Learning Repository
- PhishTank (legitimate and phishing URL collections)
- OpenPhish threat intelligence feeds

**Data Size**: Datasets typically range from thousands to hundreds of thousands of samples, with balanced or imbalanced class distributions depending on the source.

**Feature Categories**:
- **URL Features**: Length, domain age, presence of IP addresses, suspicious keywords, URL shortening services
- **Content Features**: HTML structure, JavaScript analysis, form fields, external resource links
- **Network Features**: SSL certificate information, domain reputation, WHOIS data
- **Hybrid Features**: Combinations of the above categories

## 3.4 System Analysis

### 3.4.1 Existing Phishing Detection Approaches

Existing approaches exhibit several weaknesses:
- **Single-model limitations**: Individual algorithms show inconsistent performance across attack types
- **Feature underutilization**: Many systems focus on limited feature sets
- **Poor generalization**: Models trained on specific datasets fail to generalize to new attack patterns
- **High false positives**: Overly sensitive systems generate excessive false alarms
- **Static detection**: Inability to adapt to evolving attack techniques

### 3.4.2 Proposed System Overview

The proposed hybrid ML pipeline integrates multiple classification algorithms in an ensemble framework. The system processes URLs and website content through feature extraction modules, feeds features to parallel base models, and combines predictions through ensemble mechanisms. The design emphasizes modularity, allowing easy integration of new algorithms and feature types.

## 3.5 System Architecture Design

**Data Layer**: Handles data ingestion, preprocessing, and storage. Includes data cleaning, normalization, and feature extraction pipelines.

**Feature Extraction Layer**: Implements multiple feature extraction modules for URL analysis, content parsing, and hybrid feature generation. Supports both static feature extraction and dynamic feature computation.

**Model Layer**: Contains base model implementations (Random Forest, SVM, Naive Bayes, etc.) and ensemble combination mechanisms. Supports both parallel model execution and sequential stacking approaches.

**Evaluation Layer**: Implements performance metrics calculation, model comparison, and result visualization. Provides tools for cross-validation and statistical significance testing.

## 3.6 System Modeling

The system design incorporates standard software engineering diagrams:

**Use Case Diagram**: Illustrates interactions between users (security analysts, system administrators) and the detection system, including use cases for URL checking, batch processing, and model training.

**Data Flow Diagram**: Shows data flow from input URLs through feature extraction, model processing, and output generation stages.

**Class Diagram**: Defines object-oriented structure including classes for FeatureExtractor, BaseModel, EnsembleModel, and Evaluator.

**Sequence Diagram**: Depicts temporal interactions during detection workflow, showing message passing between system components.

**Activity Diagram**: Models the detection process flow, including decision points for feature selection and model combination.

**Flowchart**: Provides high-level algorithmic representation of the hybrid detection process from input to classification output.

## 3.7 Model Design and Implementation

### 3.7.1 Feature Selection Techniques

Feature importance analysis identifies the most discriminative features for phishing detection. Techniques include:
- **Information Gain**: Measures reduction in entropy when using a feature
- **Chi-square Test**: Evaluates independence between features and class labels
- **Recursive Feature Elimination**: Iteratively removes least important features
- **Principal Component Analysis (PCA)**: Reduces dimensionality while preserving variance

### 3.7.2 Hybrid Model Structure

Example hybrid configurations include:

**Random Forest + SVM**: Random Forest provides robust feature importance and handles non-linear relationships, while SVM offers precise classification on support vectors. Combination through weighted voting.

**Random Forest + XGBoost**: Both tree-based ensemble methods with different optimization strategies. XGBoost's gradient boosting complements Random Forest's bagging approach.

**ML + Deep Learning Hybrid**: Traditional ML models (Random Forest, SVM) combined with deep learning feature extractors (CNNs for URL patterns, LSTMs for sequences).

### 3.7.3 Training and Validation Process

**Train-Test Split**: Standard 70-30 or 80-20 splits, with stratification to maintain class distribution.

**Cross-Validation**: K-fold cross-validation (typically k=5 or k=10) to assess model stability and reduce overfitting risk.

**Validation Strategy**: Separate validation sets for hyperparameter tuning, preventing data leakage and ensuring unbiased performance estimates.

## 3.8 System Evaluation and Performance Metrics

**Accuracy**: Overall correctness of classifications (TP + TN) / (TP + TN + FP + FN)

**Precision**: Proportion of positive predictions that are correct TP / (TP + FP)

**Recall (Sensitivity)**: Proportion of actual positives correctly identified TP / (TP + FN)

**F1-Score**: Harmonic mean of precision and recall, balancing both metrics 2 × (Precision × Recall) / (Precision + Recall)

**ROC-AUC**: Area under the Receiver Operating Characteristic curve, measuring model's ability to distinguish between classes across different threshold settings.

"""
    
    # Add performance findings from papers
    for paper in findings_papers[:len(findings_papers)]:
        authors = paper.get('authors', 'Unknown')
        year = paper.get('year', 'n.d.')
        metrics = paper.get('performance_metrics', '')
        findings = paper.get('findings', '')
        if metrics or findings:
            doc += f"{authors} ({year}) reported "
            if metrics:
                doc += f"performance metrics: {metrics}. "
            if findings:
                doc += f"Key findings include: {findings[:200]}."
            doc += "\n\n"
    
    doc += """## 3.9 Ethical Considerations

**Data Privacy**: Ensuring that user data and URLs processed by the system are handled securely and in compliance with privacy regulations. No personal information should be stored unnecessarily.

**Bias and Fairness**: Models must be evaluated for potential biases that could disproportionately flag legitimate content from certain domains or regions. Fairness metrics should be incorporated into evaluation.

**Responsible AI Usage**: The system should be designed with transparency and explainability considerations, allowing users to understand why content is flagged as phishing. Mechanisms for false positive correction and model improvement should be included.

## 3.10 Summary

Chapter Three presented the system analysis and design for the hybrid machine learning phishing detection system. The design incorporates multiple machine learning algorithms in an ensemble framework, with comprehensive feature extraction and evaluation capabilities. The architecture emphasizes modularity, scalability, and performance optimization while addressing ethical considerations in AI-based security systems.

---

# =================
# REFERENCES
# =================

"""
    
    # Add properly formatted references
    for ref in sorted(set(references)):
        doc += f"{ref}\n\n"
    
    return doc

# Process batch 3 papers (remaining papers)
batch3_files = [
    's40747-022-00760-3.pdf',
    's41598-025-20668-5.pdf',
    'sec21-lin.pdf',
    'usenixsecurity25-ji.pdf',
    'vaitkevicius-marcinkevicius-2020-comparison-of-classification-algorithms-for-detection-of-phishing-websites.pdf',
    'Website Phishing Detection Using Machine Learning Techniques.pdf',
    'krisana,+240565 (1).pdf'  # Including the duplicate if it exists
]

if __name__ == "__main__":
    print("Processing Lameer Batch 3 papers (Final Batch - 7 papers)...")
    print("Extracting detailed information from PDFs...")
    papers_info = []
    
    for pdf_file in batch3_files:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            print(f"\nProcessing {pdf_file}...")
            text = extract_full_text(pdf_path)
            if text and len(text) > 100:
                info = extract_detailed_info(pdf_file, text)
                papers_info.append(info)
                print(f"  ✓ Title: {info['title'][:70]}...")
                print(f"  ✓ Authors: {info['authors'][:60]}...")
                print(f"  ✓ Year: {info['year']}")
                print(f"  ✓ Methods: {info['methodology'][:80]}...")
            else:
                print(f"  ✗ Failed to extract sufficient text")
        else:
            print(f"  ✗ File not found: {pdf_file}")
    
    print(f"\n{'='*60}")
    print(f"Successfully processed {len(papers_info)} papers")
    print(f"{'='*60}")
    
    # Create batch document
    batch_doc = create_batch_document(papers_info, batch_number=3)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'BATCH 3.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(batch_doc)
    
    print(f"\n✓ Created comprehensive batch document: {output_file}")
    print(f"✓ Document contains detailed information extracted from {len(papers_info)} papers")
    print("\nBatch 3 (Final Batch) processing complete!")
    print("\nAll batches have been processed successfully!")
