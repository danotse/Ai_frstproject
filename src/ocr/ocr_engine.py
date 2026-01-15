import pytesseract
from PIL import Image
import os
import shutil

# Try to find Tesseract binary and set path if needed
def _find_tesseract():
    """Find Tesseract binary location"""
    # Common paths on macOS
    common_paths = [
        '/opt/homebrew/bin/tesseract',
        '/usr/local/bin/tesseract',
        '/usr/bin/tesseract',
    ]
    
    # Check if tesseract is in PATH
    tesseract_path = shutil.which('tesseract')
    if tesseract_path:
        return tesseract_path
    
    # Check common installation paths
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

    # Set Tesseract path if found (for local/dev environments)
tesseract_path = _find_tesseract()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text(image):
    """
    Run OCR on a preprocessed image (NumPy array or PIL Image).

    Raises a clear error if the Tesseract binary is not available so that
    the caller (e.g. Streamlit app) can show a friendly message instead of
    crashing with a low-level TesseractNotFoundError.
    """
    # Ensure we always work with a PIL Image
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)

    try:
        return pytesseract.image_to_string(image)
    except pytesseract.TesseractNotFoundError as e:
        raise RuntimeError(
            "Tesseract OCR engine is not installed or not found on this system. "
            "On Streamlit Cloud, add 'tesseract-ocr' to a packages.txt file in "
            "your repo so the system package is installed at build time."
        ) from e
