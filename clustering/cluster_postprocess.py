# cluster_postprocessing.py
import json
import re
from collections import defaultdict, Counter
from pymongo import MongoClient

CLUSTER_FILE = "clusters_out/part-00000"
RAW_DOC_FILE = "livefaq_comments.txt"

client = MongoClient("mongodb://localhost:27017/")
db = client["livefaq"]
topic_collection = db["cluster_topics"]

def load_documents():
    docs = {}
    with open(RAW_DOC_FILE, "r") as f:
        for line in f:
            doc_id, text = line.strip().split("\t", 1)
            docs[doc_id] = text.lower()
    return docs

def load_clusters():
    clusters = defaultdict(list)
    with open(CLUSTER_FILE, "r") as f:
        for line in f:
            doc_id, cid = line.strip().split("\t")
            clusters[int(cid)].append(doc_id)
    return clusters

def extract_keywords(texts):
    words = []
    for t in texts:
        t = re.sub(r"[^a-z ]", " ", t)
        words.extend(t.split())
    counter = Counter(words)
    return [w for w, _ in counter.most_common(10)]

def label_topic(keywords):
    if "spark" in keywords:
        return "Big Data Processing"
    if "youtube" in keywords or "live" in keywords:
        return "Live Streaming Queries"
    if "model" in keywords or "answer" in keywords:
        return "AI/ML Queries"
    return "General Topic"

def save_cluster_summary():
    docs = load_documents()
    clusters = load_clusters()

    output = []

    for cid, doc_ids in clusters.items():
        cluster_texts = [docs[d] for d in doc_ids if d in docs]

        keywords = extract_keywords(cluster_texts)
        topic_label = label_topic(keywords)

        summary = {
            "cluster_id": cid,
            "topic_name": topic_label,
            "keywords": keywords,
            "documents": doc_ids
        }

        topic_collection.insert_one(summary)
        output.append(summary)

        print("\nCLUSTER", cid)
        print("Keywords:", keywords)
        print("Topic:", topic_label)
        print("Documents:", len(doc_ids))

    with open("cluster_summary.json", "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    print("Post-processing Hadoop cluster output...")
    save_cluster_summary()
