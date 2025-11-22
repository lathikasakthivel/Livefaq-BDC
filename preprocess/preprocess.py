# preprocess.py
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """Perform text preprocessing: lowercasing, stopwords removal, punctuation removal."""
    if text is None:
        return ""

    text = text.lower()

    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in STOPWORDS]

    return " ".join(tokens)
