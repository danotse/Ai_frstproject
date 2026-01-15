import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.nlp.clean_text import clean as clean_text
from src.database.db_utils import save_ocr
from src.ocr.preprocess import preprocess_image
from src.ocr.ocr_engine import extract_text

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
try:
    img = preprocess_image(image_path)
except Exception as e:
    print(f"Error: Could not load or preprocess image from '{image_path}'")
    print(f"Details: {e}")
    sys.exit(1)

# OCR using the shared engine
ocr_text = extract_text(img)

# Clean text
cleaned = clean_text(ocr_text)

# Save to DB
save_ocr(image_path, ocr_text, cleaned)

print("OCR + Cleaning + Database save completed")
