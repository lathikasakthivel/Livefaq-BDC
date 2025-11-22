#!/usr/bin/env python3
# reducer.py
# LiveFAQ Hadoop Reducer – Aggregates token counts

import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t")
    count = int(count)

    if current_word and current_word != word:
        print(f"{current_word}\t{current_count}")
        current_count = 0

    current_word = word
    current_count += count

# last word
if current_word:
    print(f"{current_word}\t{current_count}")
