import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import cv2
import pytesseract
from PIL import Image

from src.nlp.clean_text import clean as clean_text
from src.database.db_utils import save_ocr

# Get image path from command line or use default
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    # Use default image in project root
    image_path = str(project_root / "image.png")

# Check if image exists
if not Path(image_path).exists():
    print(f"Error: Image file '{image_path}' not found.")
    print("Usage: python3 src/nlp/pipeline_test.py [image_path]")
    sys.exit(1)

# Load image
img = cv2.imread(image_path)
if img is None:
    print(f"Error: Could not load image from '{image_path}'")
    print("Please check that the file is a valid image.")
    sys.exit(1)

# Preprocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# OCR
ocr_text = pytesseract.image_to_string(Image.fromarray(thresh))

# Clean text
cleaned = clean_text(ocr_text)

# Save to DB
save_ocr(image_path, ocr_text, cleaned)

print("OCR + Cleaning + Database save completed")
