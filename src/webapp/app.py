import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="NoteScriber AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a modern, clean look
st.markdown("""
    <style>
    /* Main Background and Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f0f2f6;
    }

    /* Modernizing the Tabs */
    button[data-baseweb="tab"] {
        font-size: 18px;
        font-weight: 600;
        color: #475569 !important; /* Slate grey for inactive */
        padding: 10px 20px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4f46e5 !important; /* Indigo for active */
        border-bottom-color: #4f46e5 !important;
        background-color: #eff6ff;
        border-radius: 10px 10px 0 0;
    }

    /* Making Buttons Pop */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #4f46e5;
        color: white;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background-color: #4338ca;
        border: none;
        color: white;
        transform: translateY(-1px);
    }

    /* Result Card Styling */
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    <style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Center the main container */
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Modern Button Styling */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
        border: none;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    
    /* Text Areas */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)


project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from ocr.preprocess import preprocess_image
from ocr.ocr_engine import extract_text
from nlp.clean_text import clean
from nlp.summarizer import summarize
from database.insert import save_document, get_connection

def ensure_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT, ocr_text TEXT, clean_text TEXT,
            summary TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

ensure_database()

# Session State Initialization
for key in ['image_path', 'ocr_text', 'cleaned_text', 'summary', 'temp_file_path']:
    if key not in st.session_state:
        st.session_state[key] = None

# --- SIDEBAR (Modern Elements) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209265.png", width=80)
    st.title("NoteScriber AI")
    st.info("Transform your handwritten notes into digital summaries instantly.")
    
    st.divider()
    if st.button("🔄 Reset Workspace", use_container_width=True):
        if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
            try: os.unlink(st.session_state.temp_file_path)
            except: pass
        for key in st.session_state.keys():
            st.session_state[key] = None
        st.rerun()

# --- MAIN CONTENT ---
st.markdown(
    '<h1 style="color: black; margin-bottom: 0.2rem;">📝 Handwritten Notes Summarizer</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="color: black; font-size: 0.9rem; margin-top: 0;">Step-by-step AI digitizer for students and professionals</p>',
    unsafe_allow_html=True,
)

# Step 1: Upload
uploaded = st.file_uploader("Drop your note image here", type=['png', 'jpg', 'jpeg'])

if uploaded:
    if st.session_state.temp_file_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded.getbuffer())
            st.session_state.temp_file_path = tmp_file.name
            st.session_state.image_path = uploaded.name

    # Layout: Two columns for Image Preview and Action
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(uploaded, caption="Original Note", use_container_width=True)
    
    with col2:
        st.subheader("Process Image")
        if st.button("🚀 Start OCR Extraction", type="primary", use_container_width=True):
            with st.spinner("Analyzing handwriting..."):
                img = preprocess_image(st.session_state.temp_file_path)
                text = extract_text(img)
                st.session_state.ocr_text = text
                st.session_state.cleaned_text = clean(text)
                st.session_state.summary = None
            st.rerun()

    # Results Section
    if st.session_state.ocr_text:
        st.divider()
        tab1, tab2, tab3 = st.tabs(["📄 Extracted Text", "✨ Cleaned Text", "📋 AI Summary"])
        
        with tab1:
            st.text_area("Raw OCR Result", st.session_state.ocr_text, height=250)
            
        with tab2:
            st.text_area("Sanitized Version", st.session_state.cleaned_text, height=250)
            
        with tab3:
            if not st.session_state.summary:
                if st.button("✨ Generate Summary", type="primary"):
                    with st.spinner("Summarizing..."):
                        st.session_state.summary = summarize(st.session_state.cleaned_text)
                    st.rerun()
            else:
                st.markdown("### Summary")
                st.success(st.session_state.summary)
                
                if st.button("💾 Save to Database", use_container_width=True):
                    save_document(st.session_state.image_path, st.session_state.ocr_text, 
                                  st.session_state.cleaned_text, st.session_state.summary)
                    st.toast("Document saved successfully!", icon="✅")

else:
    st.info("Please upload an image to begin the digitization process.")