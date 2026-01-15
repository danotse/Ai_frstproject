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

# Set Tesseract path if found
tesseract_path = _find_tesseract()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image):
    return pytesseract.image_to_string(Image.fromarray(image))
