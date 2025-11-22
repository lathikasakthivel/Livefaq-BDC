# Big Data Concepts Used in LiveFAQ

The **LiveFAQ – Real-Time FAQ Generator for YouTube Live Streams** is built using a complete Big Data data-processing stack.  
This document explains the core Big Data concepts and how they power the project.

---

## 1. Distributed Storage (HDFS)
The project uses **Hadoop Distributed File System (HDFS)** for storing large volumes of live chat data collected from YouTube streams.

### Why HDFS?
- Handles **high-velocity data** coming from live chat.
- Fault-tolerant storage with replication.
- Enables parallel processing via MapReduce.

### How LiveFAQ uses it:
- Raw comments (`live_comments.txt`) are stored in HDFS.
- Processed comment files and TF-IDF outputs are saved back to HDFS before clustering.

---

## 2. Batch Processing (Hadoop MapReduce)
MapReduce is used for:
- Cleaning text at scale.
- Counting frequent question patterns.
- TF-IDF computation.
- Pre-clustering before model-based FAQ extraction.

### Why MapReduce?
- Efficient for massive text data.
- Fully parallel — Mapper splits text, Reducer aggregates results.
- Fault tolerant and scalable.

---

## 3. Data Transformation (Apache Pig)
Pig Latin scripts simplify preprocessing of large raw files.

### Used for:
- Removing emojis, URLs, noise.
- Extracting question-only comments.
- Filtering comments with question words (what/why/how/who…).

Pig acts as the preprocessing stage before MapReduce and clustering.

---

## 4. Stream Data Acquisition
YouTube Live APIs deliver **real-time streaming data**.

LiveFAQ implements:
- Incremental comment polling.
- Real-time streaming ingestion.
- Continuous storage into SQLite + HDFS (optional).

---

## 5. Clustering & TF-IDF Vectorization
After MapReduce processing:
- TF-IDF vectors are computed (locally or via Hadoop).
- KMeans clustering groups similar questions.
- Representative question per cluster = FAQ.

This combines **Big Data preprocessing** with **ML-based summarization**.

---

## 6. Real-Time + Batch Hybrid Architecture (Lambda Style)
- **Real-time layer**: Fetch live chat messages + store in DB.
- **Batch layer**: Hadoop/Pig pipeline runs in the background.
- **Serving layer**: Flask web app displays live FAQs + history.

This architecture ensures accuracy + scalability.

---

## Summary
| Concept | Purpose in LiveFAQ |
|--------|---------------------|
| HDFS | Distributed chat storage |
| MapReduce | Large-scale FAQ frequency computation |
| Pig | Simplified preprocessing & filtering |
| TF-IDF + KMeans | FAQ clustering & summarization |
| YouTube API | Live data ingestion |
| Flask Web App | Live dashboard & visualization |

The combination makes **LiveFAQ a complete end-to-end Big Data + ML pipeline**.
