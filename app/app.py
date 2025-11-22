#!/usr/bin/env python3
"""
app.py
Main Flask application for LiveFAQ Big Data Project.

Features:
- Fetch live YouTube comments (via API)
- Preprocess comments (emoji removal, question extraction)
- Run MapReduce-like FAQ frequency counting
- Display Live FAQs sorted by count
- Show YouTube video title
- Store FAQ history in SQLite database
"""

import json
import sqlite3
from flask import Flask, render_template, request, redirect
from datetime import datetime

# Local imports
from preprocess import preprocess_comments, clean_text, is_question
from run_livefaq_full import run_full_pipeline
from data_ingest_youtube import fetch_live_comments, fetch_video_title

app = Flask(__name__)

DB_PATH = "livefaq.db"

# -----------------------------------------------------
#  DB UTILITIES
# -----------------------------------------------------

def init_db():
    """Initialize SQLite database for FAQ history."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            video_title TEXT,
            faq_json TEXT
        );
    """)
    con.commit()
    con.close()

def save_history(video_title, faqs):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO history (timestamp, video_title, faq_json) VALUES (?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), video_title, json.dumps(faqs)))
    con.commit()
    con.close()

def load_history():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT timestamp, video_title, faq_json FROM history ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    con.close()

    history = []
    for ts, vt, fj in rows:
        history.append({
            "timestamp": ts,
            "video_title": vt,
            "faqs": json.loads(fj)
        })
    return history


# -----------------------------------------------------
# ROUTES
# -----------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_id = request.form.get("video_id")

        # 1. Fetch comments + title
        comments = fetch_live_comments(video_id)
        video_title = fetch_video_title(video_id)

        # 2. Preprocess comments into questions
        question_candidates = preprocess_comments([c["text"] for c in comments])

        # 3. Run full Hadoop → TF-IDF → Clustering pipeline
        faq_counts = run_full_pipeline(question_candidates)

        # 4. Save to history
        save_history(video_title, faq_counts)

        return render_template("live.html",
                               video_title=video_title,
                               faqs=faq_counts,
                               video_id=video_id)

    return render_template("index.html")


@app.route("/history")
def history():
    data = load_history()
    return render_template("history.html", history=data)


@app.route("/stop")
def stop():
    return redirect("/")


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------

if __name__ == "__main__":
    print("Initializing LiveFAQ database...")
    init_db()
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=False)
