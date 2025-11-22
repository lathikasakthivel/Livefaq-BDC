# FAQ Pipeline Explained

## 1. Introduction

The LiveFAQ Big Data Pipeline processes large volumes of FAQ text, chat queries, and YouTube transcripts to generate:

- Cleaned & preprocessed text
- TF-IDF vector representations
- Query clusters (K-Means)
- Real-time FAQ recommendations
- Query history analytics

This document explains the complete data pipeline used in the project.

## 2. High-Level Architecture

```mermaid
graph TD
    A[Raw Data
    FAQ, YouTube, Live Chat] --> B[Preprocessing (Python)]
    B --> C[HDFS Storage]
    C --> D[MapReduce (TF-IDF)]
    D --> E[Cluster Post-processing]
    E --> F[FAQ Vector Store & API]
    F --> G[Web App
    Search + Live FAQ]
```

## 3. Pipeline Components Explained

### 3.1 Data Ingestion

**Sources include:**
- Stored FAQs (`faq_data/faq.txt`)
- YouTube Captions (via `data_ingest_youtube.py`)
- Live chat queries (user search queries)

**HDFS Storage Command:**
```bash
hdfs dfs -put faq.txt /livefaq/input/
```

**Purpose:** Enables distributed processing of large text data.

### 3.2 Preprocessing (`preprocess.py`)

**Tasks:**
- Lowercasing
- Removing punctuation
- Tokenization
- Stopword removal
- Lemmatization

**Output Format:**
```
docID<TAB>cleaned text
```

### 3.3 Hadoop MapReduce (TF-IDF Calculation)

#### JOB 1 – Term Frequency (TF)
- **Mapper**: Splits documents into words
- **Reducer**: Counts word occurrences

**Output:**
```
docID:word   TF
```

#### JOB 2 – TF-IDF + Vector Generation
- **Mapper**: Reorganizes TF data
- **Reducer**: Calculates:
  - Total documents
  - IDF (Inverse Document Frequency)
  - TF-IDF scores

**Output:**
```
docID   [0.34, 0.12, 0.88, ...]
```

**Storage Location:**
```
/livefaq/output/tfidf_vectors/
```

### 3.4 Clustering (`mr_tfidf_kmeans.py`)

- Performs K-Means clustering on TF-IDF vectors
- Groups questions into k categories (e.g., 8)
- Assigns vectors to nearest centroid

**Output Format:**
```
cluster_id   docID   keywords
```

**Storage Location:**
```
/livefaq/output/clusters/
```

### 3.5 Cluster Post-processing (`cluster_postprocessing.py`)

**Purpose:**
- Extract top keywords
- Summarize each cluster
- Auto-generate FAQ titles

**Example Output:**
```
Cluster 3 - "Refund & Payment Issues"
Top Keywords: refund, payment, processing, delay
```

### 3.6 API Layer (FastAPI – `app.py`)

**Endpoints:**
- Search endpoint
- Live FAQ query endpoint
- Cluster fetch endpoint
- Query history visualization

**Example Request:**
```http
GET /search?query=how%20to%20refund
```

**Response:**
```json
{
  "faq": "Refund Process – Steps to Follow",
  "confidence": 0.92,
  "cluster": "Payments & Refund",
  "similar_questions": [...]
}
```

### 3.7 Frontend Templates

| File | Purpose |
|------|---------|
| `index.html` | Main FAQ search interface |
| `live.html` | Real-time FAQ suggestions |
| `history.html` | Analytics & user activity |

## 4. End-to-End Pipeline Example

### Input
User query: "How can I get my refund?"

### Pipeline Execution
1. Preprocessing → "get refund"
2. Convert to TF-IDF vector
3. Match with nearest cluster
4. Retrieve best-ranked FAQ
5. Display answer and similar questions

### Final Output
```
Best Match: "Refund Process – Steps to Follow"
Cluster: "Payments & Refund"
Confidence: 92%
```

## 5. How the Pipeline Supports LiveFAQ

### Scalability
Hadoop MapReduce enables handling of:
- Thousands of questions
- Long YouTube transcripts
- Continuous chat inputs

### Accuracy
TF-IDF + clustering improves:
- Search relevance
- Query similarity detection
- Topic-based grouping

### Automation
The system automatically:
- Creates FAQ clusters
- Summarizes topics
- Generates insights for UI

### Real-Time Performance
FastAPI + vector lookup ensures fast response (20–40ms).

## 6. Key Observations

1. The pipeline efficiently processes large text datasets using Hadoop MapReduce
2. Preprocessing, TF-IDF, and clustering enable accurate FAQ grouping
3. Distributed computation significantly reduces processing time
4. Real-time FastAPI integration ensures instant FAQ retrieval
5. The system provides relevant, context-aware recommendations