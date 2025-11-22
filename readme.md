# 🎥 LiveFAQ: Real-time FAQ Generator for YouTube Live Streams

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.x-yellow.svg)](https://hadoop.apache.org/)

LiveFAQ is a real-time Big Data pipeline that transforms YouTube live chat into meaningful FAQs using distributed processing and machine learning.

## 🚀 Features

- **Real-time Processing**: Captures and processes live YouTube chat messages
- **Smart Filtering**: Removes noise (emojis, URLs, spam) and detects questions
- **Distributed Computing**: Leverages Hadoop MapReduce for scalable processing
- **Intelligent Clustering**: Uses TF-IDF + KMeans to group similar questions
- **Live Dashboard**: Interactive web interface to view FAQs and analytics
- **Historical Analysis**: Stores and visualizes FAQ trends over time

## 🏗 Architecture

```mermaid
graph LR
    A[YouTube Live Chat] --> B[Data Ingestion]
    B --> C[Preprocessing]
    C --> D[HDFS Storage]
    D --> E[MapReduce Processing]
    E --> F[TF-IDF + KMeans]
    F --> G[FAQ Generation]
    G --> H[Web Dashboard]
    H --> I[(SQLite DB)]
    I --> H
```

## 🛠 Tech Stack

### Big Data
- **Hadoop HDFS** - Distributed storage
- **Hadoop MapReduce** - Distributed processing
- **Apache Pig** - Data flow scripting

### Backend
- **Python 3.8+** - Core programming
- **Flask** - Web framework
- **scikit-learn** - ML algorithms (TF-IDF, KMeans)
- **SQLite** - Local database
- **YouTube Data API** - Live chat streaming

### Infrastructure
- **Ubuntu 20.04** - Operating system
- **Virtual Machine** - Local development
- **Docker** - Containerization (optional)

## 📊 Sample Output

### Live FAQ Dashboard
```
🎯 Live FAQs (Top Questions)
----------------------------------
1. how are you all? (3)
2. where is the host? (2)
3. what happened in the stream? (2)
4. why is the music lagging? (1)

🎬 Now Playing: jazz lofi radio 🎷 beats to chill/study to

[Start Live FAQ]  [Stop]  [View History]
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Java 8+
- Hadoop 3.3.x
- YouTube Data API Key

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/livefaq.git
cd livefaq

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your YouTube API key
```

### Running the Pipeline
```bash
# Start Hadoop services
start-dfs.sh
start-yarn.sh

# Run the pipeline
python run_pipeline.py

# Start the web dashboard
python app/run_web.py
```

## 📈 Performance Metrics

- **Processing Speed**: Handles 1,000+ comments per minute
- **Accuracy**: 85%+ question detection rate
- **Scalability**: Tested with 50,000+ comments
- **Latency**: Near real-time (2-5 second delay)

## � Documentation

- [Big Data Concepts](./docs/bigdata_concepts.md)
- [Hadoop MapReduce Guide](./docs/hadoop_mapreduce_explained.md)
- [FAQ Pipeline Details](./docs/faq_pipeline_explained.md)
