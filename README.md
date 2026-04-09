# Digital Health App Privacy Compliance Analysis

A multi-method NLP and LLM pipeline for detecting inconsistencies between declared health data permissions and privacy policy disclosures in mobile health Android apps.

## Overview

Mobile health apps frequently request sensitive health permissions (Steps, Heart Rate, Sleep, etc.) without adequately disclosing data collection practices in their privacy policies. This project systematically audits 32 health Android apps using three complementary approaches: rule-based keyword matching, machine learning classification, and zero-shot LLM-based extraction.

**Why it matters:**
Health apps handle highly sensitive personal data, yet lack of transparency in privacy disclosures can pose significant risks to users and regulators. This project demonstrates how automated methods can be used to audit privacy compliance at scale, providing a foundation for improving accountability in digital health ecosystems.

**Key findings:**
- **96.9%** of analyzed apps exhibited at least one inconsistency between declared permissions and policy disclosures
- TF-IDF + Logistic Regression baseline achieved **42% accuracy**, demonstrating the limitations of surface-level text features for semantic compliance detection
- Zero-shot LLM pipeline confirmed only **10 out of 76** permission checks were explicitly disclosed in policy text, indicating systematic under-disclosure of health data collection practices

## Project Structure

```
├── keyword_matching.py     # Rule-based NLP pipeline with verb-category and negation detection
├── ml_baseline.py          # TF-IDF + Logistic Regression classifier
├── privacy_analysis.py     # Zero-shot LLM pipeline using Gemini API via Vertex AI
├── convert.py              # Data conversion: JSONL → CSV and HTML viewer
├── Labeled_pairs.csv       # 77 manually labeled permission-policy pairs (YES/NO/PARTIAL)
└── README.md
```

## Methods

### 1. Keyword Matching Baseline (`keyword_matching.py`)
Rule-based pipeline inspired by [PolicyChecker (Xiang, Pei, Yue — CCS 2023)](https://dl.acm.org/doi/10.1145/3576915.3616679).

- **Triple-condition matching** per sentence: verb + data keyword + negation check
- Verb categories: collection (collect/gather/record), sharing (share/disclose/transfer), retention (retain/hold/keep)
- Data keywords defined per permission type: Steps, Distance, Heart rate, Calories, Sleep, Weight
- Detects two violation types:
  - Type 1: Permission declared but not mentioned in policy
  - Type 2: Data mentioned in policy but permission not declared

### 2. ML Baseline (`ml_baseline.py`)
TF-IDF + Logistic Regression classifier trained on manually labeled data.

- **Input:** 77 labeled permission-policy text pairs
- **Features:** TF-IDF vectors (max 2,000 features, unigrams + bigrams)
- **Labels:** YES / NO / PARTIAL
- **Result:** 42% accuracy — revealing that surface-level text features are insufficient for semantic compliance detection

### 3. LLM-based Extraction (`privacy_analysis.py`)
Zero-shot LLM pipeline using Gemini API via Google Cloud Vertex AI.

- Model: `gemini-2.5-flash-lite`
- Prompt engineering: zero-shot, structured output format (Permission / Status / Reason)
- Extracts semantic understanding of health data disclosures from unstructured policy text
- Scalable to large datasets without labeled training data

## Setup

### Requirements
```bash
pip install google-cloud-aiplatform pandas scikit-learn
```

### Authentication (Vertex AI)
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
export GCP_PROJECT_ID="your-project-id"
```

### Run

```bash
# Keyword matching
python keyword_matching.py

# ML baseline (requires Labeled_pairs.csv)
python ml_baseline.py

# LLM pipeline (requires Vertex AI authentication)
python privacy_analysis.py
```

## Results Summary

| Method | Coverage | Key Result |
|--------|----------|------------|
| Keyword Matching | 32 apps | 96.9% have compliance gaps |
| TF-IDF + LR | 77 labeled pairs | 42% accuracy |
| Zero-shot LLM | 31 apps, 76 checks | 10/76 permissions explicitly disclosed |

## Data

The dataset consists of 32 mobile health Android apps with the following fields:
- `packagename`: Android app package identifier
- `pp`: Full privacy policy text
- `declared_permission`: List of health permissions declared in the app manifest

Raw data files are not included in this repository. `Labeled_pairs.csv` contains 77 manually annotated permission-policy text pairs used for ML baseline training and evaluation.

## Reference

- Xiang, G., Pei, K., & Yue, C. (2023). PolicyChecker: Analyzing the GDPR Completeness of Mobile Apps' Privacy Policies. *ACM CCS 2023*.
