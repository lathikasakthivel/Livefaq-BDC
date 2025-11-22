# 🚀 LiveFAQ Project — Complete Setup Guide (Ubuntu 20.04 / 22.04)

This guide explains how to install and configure all components required to run the LiveFAQ Big Data Pipeline.

## 📋 Table of Contents
1. [System Requirements](#-1-system-requirements)
2. [Python & Virtual Environment](#-2-python--virtual-environment)
3. [Install Java](#-3-install-java)
4. [Install Hadoop](#-4-install-hadoop-33x)
5. [Configure Hadoop](#-5-configure-hadoop-single-node-mode)
6. [Install Apache Pig](#-6-install-apache-pig)
7. [YouTube API Setup](#-7-youtube-api-setup-live-chat)
8. [Run Live Data Ingestion](#-8-run-live-data-ingestion)
9. [Preprocess Comments](#-9-preprocess-comments)
10. [Run Hadoop MapReduce](#-10-run-hadoop-mapreduce-faq-counting)
11. [Run TF-IDF + K-Means Clustering](#-11-run-tf-idf--k-means-clustering)
12. [Launch the LiveFAQ Web App](#-12-launch-the-livefaq-web-app)
13. [Complete End-to-End Pipeline](#-13-complete-end-to-end-pipeline-command)
14. [Testing the Setup](#-14-testing-the-setup)
15. [Troubleshooting](#-15-troubleshooting)

## 🧩 1. System Requirements

### ✔ Recommended System
- **OS**: Ubuntu 20.04 / 22.04 (VM or Physical Machine)
- **RAM**: 4 GB (Minimum)
- **Storage**: 20 GB
- **Internet**: Stable connection required

## 🐍 2. Python & Virtual Environment

### Install Python 3 & pip
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Create & Activate Virtual Environment
```bash
python3 -m venv livefaq-venv
source livefaq-venv/bin/activate
```

### Install Project Dependencies
```bash
pip install -r requirements.txt
```

## 🏗️ 3. Install Java

```bash
sudo apt install openjdk-11-jdk -y
java -version
```

## 🏛️ 4. Install Hadoop 3.3.x

### Download Hadoop
```bash
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 ~/hadoop
```

### Add Environment Variables
Add to `~/.bashrc`:
```bash
export HADOOP_HOME=~/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

Reload config:
```bash
source ~/.bashrc
```

## 📂 5. Configure Hadoop (Single Node Mode)

### Edit hadoop-env.sh
```bash
nano ~/hadoop/etc/hadoop/hadoop-env.sh
```
Add:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Format the NameNode
```bash
hdfs namenode -format
```

### Start Hadoop Services
```bash
start-dfs.sh
start-yarn.sh
```

### Verify Running Services
```bash
jps
```
You should see:
- NameNode
- DataNode
- ResourceManager
- NodeManager

## 🐷 6. Install Apache Pig

### Download Pig
```bash
wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz
tar -xzf pig-0.17.0.tar.gz
mv pig-0.17.0 ~/pig
```

### Add Pig to PATH
Add to `~/.bashrc`:
```bash
export PIG_HOME=~/pig
export PATH=$PATH:$PIG_HOME/bin
```
Reload:
```bash
source ~/.bashrc
```

### Verify Pig Installation
```bash
pig -version
```

## 🎥 7. YouTube API Setup (Live Chat)
1. **Enable YouTube Data API v3**
   - Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs → Enable YouTube Data API v3

2. **Create API Key**
   - Go to: Credentials → Create Credentials → API Key

3. **Save API key in `.env`**
   ```
   YOUTUBE_API_KEY=YOUR_KEY_HERE
   ```

## 📥 8. Run Live Data Ingestion
```bash
python ingest/data_ingest_youtube.py
```
**Output:** `live_comments.txt`

## 🧹 9. Preprocess Comments
```bash
python preprocess/preprocess.py
```
**Output:** `clean_comments.txt`

## 🗂️ 10. Run Hadoop MapReduce (FAQ Counting)

### Put cleaned data into HDFS
```bash
hdfs dfs -mkdir /faq
hdfs dfs -put clean_comments.txt /faq/input.txt
```

### Run MapReduce
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper mapper.py \
  -reducer reducer.py \
  -input /faq/input.txt \
  -output /faq/output
```

### Fetch Results
```bash
hdfs dfs -cat /faq/output/part-00000 > faq_counts.txt
```

## 🧠 11. Run TF-IDF + K-Means Clustering
```bash
python clustering/mr_tfidf_kmeans.py
```
**Output:** `clusters.jsonl`

## 🌐 12. Launch the LiveFAQ Web App
```bash
python app/run_livefaq_web.py
```
Access at: http://localhost:5000

### Features:
- Live FAQ list
- Bar/Pie charts
- Video title display
- History tracking
- Auto-refresh functionality

## 🎉 13. Complete End-to-End Pipeline Command

Run the entire pipeline with one command:
```bash
python ingest/data_ingest_youtube.py && \
python preprocess/preprocess.py && \
sh mapreduce/hadoop_run.sh && \
python clustering/mr_tfidf_kmeans.py && \
python app/run_livefaq_web.py
```

## 🧪 14. Testing the Setup

### Using Sample File
```bash
python preprocess/test_preprocess.py
```
**Test File:** `ingest/sample_live_comments.jsonl`

## 🛠️ 15. Troubleshooting

### ❗ Hadoop command not found
```bash
source ~/.bashrc
```

### ❗ Java not detected
```bash
sudo update-alternatives --config java
```

### ❗ Pig "JAVA_HOME not set"
Add to `pig-env.sh`:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### ❗ No live comments fetching
Possible causes:
- API key expired
- Live stream not enabled for chat
- Incorrect broadcast ID