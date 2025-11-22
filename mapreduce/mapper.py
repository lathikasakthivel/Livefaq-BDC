#!/usr/bin/env python3
# mapper.py
# LiveFAQ Hadoop Mapper – Cleans text, removes emojis, tokenizes words

import sys
import re

# Emoji removal pattern
EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

# URL removal
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

# Normalize and tokenize
def clean_and_tokenize(text):
    text = text.lower()
    text = URL_PATTERN.sub("", text)
    text = EMOJI_PATTERN.sub("", text)
    text = re.sub(r"[^a-z0-9? ]", " ", text)  # keep ? for question detection
    return text.split()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    tokens = clean_and_tokenize(line)

    for t in tokens:
        if len(t) > 1:     # avoid noise: a, m, k etc.
            print(f"{t}\t1")
