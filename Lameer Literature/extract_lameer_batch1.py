#!/usr/bin/env python3
"""
Script to extract and analyze 15 papers for Hybrid Machine Learning Model for Phishing Detection
Creates a comprehensive batch synthesis document
"""
import PyPDF2
import re
import os
from datetime import datetime

def extract_full_text(pdf_file):
    """Extract full text from PDF"""
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''.join([page.extract_text() for page in reader.pages])
            return text
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return ""

def extract_paper_info(pdf_file, text):
    """Extract structured information from paper"""
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
        'full_text': text[:50000]  # Limit text for analysis
    }
    
    # Extract title
    lines = [l.strip() for l in text.split('\n')[:50] if len(l.strip()) > 15]
    if lines:
        info['title'] = lines[0][:300]
    
    # Extract year
    year_match = re.search(r'\b(20\d{2})\b', text[:5000])
    if year_match:
        info['year'] = year_match.group(1)
    
    # Extract authors
    author_patterns = [
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+and\s+[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
        r'Author[s]?[:\s]+([^\n]{10,200})',
        r'By\s+([^\n]{10,200})',
    ]
    for pattern in author_patterns:
        match = re.search(pattern, text[:3000], re.IGNORECASE)
        if match and len(match.group(1)) > 5:
            info['authors'] = match.group(1).strip()[:200]
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
            info['abstract'] = abstract[:2000]
            break
    
    # Extract source/journal
    source_patterns = [
        r'Journal\s+of\s+([^\n]{5,100})',
        r'Proceedings\s+of\s+([^\n]{5,100})',
        r'Conference\s+on\s+([^\n]{5,100})',
        r'IEEE\s+([^\n]{5,100})',
        r'arXiv:([^\n]{5,50})',
    ]
    for pattern in source_patterns:
        match = re.search(pattern, text[:5000], re.IGNORECASE)
        if match:
            info['source'] = match.group(0).strip()[:200]
            break
    
    # Extract methodology
    ml_keywords = ['machine learning', 'deep learning', 'SVM', 'Random Forest', 'Naive Bayes', 
                   'Decision Tree', 'CNN', 'RNN', 'LSTM', 'hybrid', 'ensemble', 'XGBoost',
                   'phishing detection', 'classification', 'feature extraction']
    found_methods = [kw for kw in ml_keywords if kw.lower() in text.lower()[:10000]]
    if found_methods:
        info['methodology'] = ", ".join(set(found_methods[:10]))
    
    # Extract dataset mentions
    dataset_patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+dataset)',
        r'(Kaggle|UCI|PhishTank|OpenPhish)',
        r'(\d+[,\.]\d+\s*(?:million|thousand|K|M)\s*samples?)',
    ]
    datasets = []
    for pattern in dataset_patterns:
        matches = re.findall(pattern, text[:10000], re.IGNORECASE)
        datasets.extend(matches)
    if datasets:
        info['dataset'] = ", ".join(set(datasets[:5]))
    
    # Extract limitations
    limitation_keywords = ['limitation', 'challenge', 'drawback', 'weakness', 'future work']
    limitation_sections = []
    for keyword in limitation_keywords:
        pattern = rf'{keyword}[:\s]+(.*?)(?:\.\s+[A-Z]|Conclusion|References)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            limitation_sections.append(match.group(1).strip()[:500])
    if limitation_sections:
        info['limitations'] = " ".join(limitation_sections[:2])
    
    return info

def create_batch_document(papers_info, batch_number=1):
    """Create comprehensive batch synthesis document"""
    
    # Extract relevant content for each section
    background_info = []
    problem_statements = []
    methodologies = []
    datasets_mentioned = []
    limitations_list = []
    gaps_identified = []
    
    for paper in papers_info:
        text_lower = (paper['abstract'] + " " + paper['full_text']).lower()
        
        # Background information
        if any(term in text_lower for term in ['phishing', 'cybersecurity', 'threat', 'attack']):
            background_info.append({
                'author': paper['authors'],
                'year': paper['year'],
                'content': paper['abstract'][:300]
            })
        
        # Problem statements
        if any(term in text_lower for term in ['false positive', 'zero-day', 'concept drift', 'limitation', 'challenge']):
            problem_statements.append({
                'author': paper['authors'],
                'year': paper['year'],
                'content': paper['limitations'] if paper['limitations'] else paper['abstract'][:300]
            })
        
        # Methodologies
        if paper['methodology']:
            methodologies.append({
                'author': paper['authors'],
                'year': paper['year'],
                'method': paper['methodology'],
                'title': paper['title']
            })
        
        # Datasets
        if paper['dataset']:
            datasets_mentioned.append({
                'author': paper['authors'],
                'year': paper['year'],
                'dataset': paper['dataset']
            })
        
        # Limitations and gaps
        if paper['limitations']:
            limitations_list.append({
                'author': paper['authors'],
                'year': paper['year'],
                'limitation': paper['limitations'][:400],
                'method': paper['methodology']
            })
    
    # Generate APA references
    references = []
    for paper in papers_info:
        if paper['authors'] != "Not found" and paper['year'] != "Not found":
            ref = f"{paper['authors']} ({paper['year']}). {paper['title']}. {paper['source']}."
            references.append(ref)
    
    # Create the document
    doc = f"""# BATCH {batch_number}: Hybrid Machine Learning Model for Phishing Detection
## Literature Review Synthesis Document

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

{chr(10).join([f"- {item['author']} ({item['year']}) highlighted that {item['content'][:200]}..." for item in background_info[:3]])}

## 1.2 Statement of the Problem

The research literature reveals several critical problems in current phishing detection systems that necessitate the development of hybrid machine learning approaches:

**High False Positive Rates**: Existing detection systems frequently misclassify legitimate websites as phishing sites, leading to user frustration and reduced trust in security systems. This problem undermines the practical utility of detection mechanisms in real-world deployments.

**Zero-Day Phishing Attacks**: Traditional detection methods fail to identify previously unseen phishing attacks, creating significant security gaps. Attackers continuously develop novel techniques that bypass existing detection signatures, necessitating adaptive detection capabilities.

**Concept Drift**: Phishing attack patterns evolve over time, causing previously effective detection models to degrade in performance. This temporal drift requires continuous model retraining and adaptation, which single-model approaches struggle to accommodate effectively.

**Poor Generalization of Single ML Models**: Individual machine learning algorithms demonstrate inconsistent performance across different phishing attack types and datasets. Some models excel at detecting certain attack patterns while failing on others, indicating the need for complementary model combinations.

**Limited Feature Utilization**: Single models may not effectively leverage the diverse feature sets available for phishing detection, including URL characteristics, content analysis, and behavioral patterns. Hybrid approaches can better integrate multiple feature types.

{chr(10).join([f"- {item['author']} ({item['year']}) identified that {item['content'][:200]}..." for item in problem_statements[:3]])}

The research gap motivating hybrid machine learning models lies in the need for robust, adaptive detection systems that can effectively combine multiple algorithms to achieve superior performance compared to individual models while maintaining practical applicability in real-world scenarios.

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

**Support Vector Machines (SVM)**: SVM classifiers have been widely applied to phishing detection, demonstrating good performance on high-dimensional feature spaces. They work by finding optimal hyperplanes that separate phishing and legitimate instances.

**Naive Bayes**: Probabilistic classifiers that assume feature independence. While this assumption is often violated, Naive Bayes models remain popular due to computational efficiency and reasonable performance on phishing datasets.

**Decision Trees**: Tree-based models that provide interpretable decision rules. They recursively partition the feature space based on feature values to classify instances.

**Random Forest**: Ensemble of decision trees that reduces overfitting through aggregation. Random Forest has shown strong performance in phishing detection tasks, handling non-linear relationships and feature interactions effectively.

### 2.3.3 Deep Learning Approaches

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
    
    # Add research gaps table entries
    for i, paper in enumerate(limitations_list[:15], 1):
        method = paper.get('method', 'Not specified')
        dataset = next((d['dataset'] for d in datasets_mentioned if d['author'] == paper['author']), 'Not specified')
        limitation = paper['limitation'][:100] if paper['limitation'] else 'Not specified'
        gap = "Need for hybrid approaches" if 'single' in method.lower() or 'individual' in method.lower() else "Generalization and robustness"
        
        doc += f"| {paper['author']} ({paper['year']}) | {method[:50]} | {dataset[:50]} | {limitation[:80]} | {gap} |\n"
    
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
- Kaggle phishing datasets
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

## 3.9 Ethical Considerations

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
    
    # Add references
    for ref in references:
        doc += f"{ref}\n\n"
    
    return doc

# Process first 15 papers
batch1_files = [
    '1.pdf',
    '10115_2022_Article_1672.pdf',
    '10586_2022_Article_3604.pdf',
    '11235_2020_Article_733.pdf',
    '2009.11116v1.pdf',
    '20250911153152_FMR-2025-2-095.1.pdf',
    '2101.02552v1.pdf',
    '2201.10752v1.pdf',
    '40745_2022_Article_379.pdf',
    '767f1a0b59241845f47547ff90cac3042afd.pdf',
    'A novel approach for phishing URLs detection using lexical.pdf',
    'A_novel_hybrid_approach_of_SVM_combined.pdf',
    'A-literature-review-on-classification-of-phishing-attacks.pdf',
    'Adebowale_2020 (1).pdf',
    'Adebowale_2020.pdf'
]

if __name__ == "__main__":
    print("Processing Lameer Batch 1 papers (15 papers)...")
    papers_info = []
    
    for pdf_file in batch1_files:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            print(f"Processing {pdf_file}...")
            text = extract_full_text(pdf_path)
            if text and len(text) > 100:
                info = extract_paper_info(pdf_file, text)
                papers_info.append(info)
                print(f"  ✓ Extracted: {info['title'][:60]}...")
            else:
                print(f"  ✗ Failed to extract sufficient text")
        else:
            print(f"  ✗ File not found: {pdf_file}")
    
    print(f"\nSuccessfully processed {len(papers_info)} papers")
    
    # Create batch document
    batch_doc = create_batch_document(papers_info, batch_number=1)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'BATCH 1.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(batch_doc)
    
    print(f"\n✓ Created: {output_file}")
    print("Batch 1 processing complete!")
