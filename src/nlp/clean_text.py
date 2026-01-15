import re

def clean(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)
    return text.strip()
