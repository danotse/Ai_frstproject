import os
import streamlit as st
from transformers import pipeline

# -----------------------
# Cached loader (Streamlit-safe)
# -----------------------
@st.cache_resource
def load_summarizer(model_name: str):
    """Load and cache a summarization pipeline for the given model name."""
    return pipeline("summarization", model=model_name)


def get_summarizer():
    """
    Choose a model based on the environment variable USE_FAST_MODEL.
    Try the preferred model first, then fall back to smaller models if loading fails.
    """
    use_fast_model = os.getenv("USE_FAST_MODEL", "true").lower() == "true"
    preferred = "sshleifer/distilbart-cnn-12-6" if use_fast_model else "facebook/bart-large-cnn"

    # Try preferred model
    try:
        return load_summarizer(preferred)
    except Exception as e:
        # Fallback order
        fallback_candidates = ["sshleifer/distilbart-cnn-12-6", "google/pegasus-xsum"]
        # Ensure preferred isn't duplicated in the list
        for candidate in fallback_candidates:
            if candidate == preferred:
                continue
            try:
                st.warning(f"Could not load {preferred}: {e}. Falling back to {candidate}.")
                return load_summarizer(candidate)
            except Exception as e2:
                # Try next fallback
                last_err = e2
                continue

        # If nothing worked, raise the last error so caller can handle it
        raise RuntimeError(f"Could not load any summarization model. Last error: {last_err}")


# -----------------------
# Text cleaning + trimming
# -----------------------
def clean_and_trim_text(text: str, max_words: int = 400) -> str:
    """Normalize whitespace and trim to max_words to avoid huge transformer inputs."""
    if not text:
        return ""
    text = text.replace("\n", " ")
    text = " ".join(text.split())  # collapse multiple spaces
    words = text.split()
    return " ".join(words[:max_words])


# -----------------------
# Summarization function
# -----------------------
def summarize(text: str) -> str:
    """
    Summarize the given text.
    - Cleans and trims input (prevents very long inputs).
    - Uses Streamlit-cached summarizer.
    - Uses truncation=True to prevent tokenizer overflow issues.
    """
    if not text or len(text.strip()) < 50:
        return "Text is too short to summarize."

    cleaned = clean_and_trim_text(text, max_words=400)

    try:
        summarizer = get_summarizer()
    except Exception as e:
        return f"Summarization model load failed: {e}"

    try:
        # trunkation=True ensures the tokenizer will truncate inputs longer than max model length
        result = summarizer(
            cleaned,
            max_length=120,
            min_length=40,
            truncation=True,
            do_sample=False
        )
        return result[0].get("summary_text", "").strip()
    except Exception as e:
        return f"Summarization failed: {e}"
