#!/usr/bin/env python3
# mr_tfidf_kmeans.py
# Hadoop Streaming MapReduce: TF-IDF + KMeans Clustering

import sys
import math
import json
from collections import defaultdict

K = 3  # number of clusters
CENTROID_FILE = "centroids.json"

def load_centroids():
    """Load centroid vectors from JSON file."""
    try:
        with open(CENTROID_FILE, "r") as f:
            return json.load(f)
    except:
        # default centroids (random initialization)
        return [
            {"id": 0, "vector": {"data": 1, "error": 0}},
            {"id": 1, "vector": {"live": 1, "youtube": 0}},
            {"id": 2, "vector": {"spark": 1, "model": 0}},
        ]

CENTROIDS = load_centroids()

def tokenize(text):
    text = text.lower()
    for ch in ",.:;!?":
        text = text.replace(ch, "")
    return text.split()

# ------------------------ MAPPER ------------------------

def mapper():
    for line in sys.stdin:
        parts = line.strip().split("\t", 1)
        if len(parts) != 2:
            continue

        doc_id, text = parts
        tokens = tokenize(text)

        tf = defaultdict(int)
        for t in tokens:
            tf[t] += 1

        # emit term frequency
        for term, freq in tf.items():
            print(f"{term}\t{doc_id}:{freq}")

# ------------------------ REDUCER: BUILD TF-IDF ------------------------

def reducer_tfidf():
    current_term = None
    docs = defaultdict(int)

    for line in sys.stdin:
        term, docfreq = line.strip().split("\t")
        doc_id, freq = docfreq.split(":")
        freq = int(freq)

        if current_term and current_term != term:
            # compute TF-IDF
            df = len(docs)
            idf = math.log(1 + (1000 / (df + 1)))

            for doc, f in docs.items():
                tfidf = f * idf
                print(f"{doc}\t{current_term}:{tfidf}")

            docs = defaultdict(int)

        current_term = term
        docs[doc_id] += freq

    # last term
    if current_term:
        df = len(docs)
        idf = math.log(1 + (1000 / (df + 1)))
        for doc, f in docs.items():
            tfidf = f * idf
            print(f"{doc}\t{current_term}:{tfidf}")


# -------------------- REDUCER 2: ASSIGN CLUSTER --------------------

def parse_vector(kv_list):
    vector = {}
    for kv in kv_list:
        term, val = kv.split(":")
        vector[term] = float(val)
    return vector

def vector_distance(v1, v2):
    keys = set(v1.keys()).union(v2.keys())
    return math.sqrt(sum((v1.get(k, 0) - v2.get(k, 0)) ** 2 for k in keys))

def reducer_cluster():
    """Assign each doc to the closest centroid."""
    current_doc = None
    vec_entries = []

    for line in sys.stdin:
        doc, termval = line.strip().split("\t")

        if current_doc and current_doc != doc:
            vector = parse_vector(vec_entries)

            closest, dist = -1, float("inf")
            for centroid in CENTROIDS:
                cvec = centroid["vector"]
                d = vector_distance(vector, cvec)
                if d < dist:
                    closest = centroid["id"]
                    dist = d

            print(f"{current_doc}\t{closest}")

            vec_entries = []

        current_doc = doc
        vec_entries.append(termval)

    # last doc
    if current_doc:
        vector = parse_vector(vec_entries)
        closest, dist = -1, float("inf")
        for centroid in CENTROIDS:
            cvec = centroid["vector"]
            d = vector_distance(vector, cvec)
            if d < dist:
                closest = centroid["id"]
                dist = d

        print(f"{current_doc}\t{closest}")


# ------------------------ MAIN ------------------------

if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "map":
        mapper()
    elif mode == "tfidf":
        reducer_tfidf()
    elif mode == "cluster":
        reducer_cluster()
    else:
        print("Invalid mode. Use: map | tfidf | cluster", file=sys.stderr)
