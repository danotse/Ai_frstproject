import sys
import os

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ocr.preprocess import preprocess_image
from ocr.ocr_engine import extract_text
from nlp.clean_text import clean

def test_ocr(image_path):
    """
    Test OCR functionality with a given image path.
    
    Args:
        image_path: Path to the image file to test
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        print("Please provide a valid path to an image file.")
        return
    
    print(f"Testing OCR on: {image_path}")
    print("-" * 50)
    
    try:
        # Step 1: Preprocess the image
        print("Step 1: Preprocessing image...")
        preprocessed_img = preprocess_image(image_path)
        print("✓ Image preprocessed successfully")
        
        # Step 2: Extract text using OCR
        print("\nStep 2: Extracting text with OCR...")
        extracted_text = extract_text(preprocessed_img)
        print("✓ Text extracted successfully")
        
        # Step 3: Clean the text
        print("\nStep 3: Cleaning text...")
        cleaned_text = clean(extracted_text)
        print("✓ Text cleaned successfully")
        
        # Display results
        print("\n" + "=" * 50)
        print("EXTRACTED TEXT:")
        print("=" * 50)
        print(extracted_text)
        print("\n" + "=" * 50)
        print("CLEANED TEXT:")
        print("=" * 50)
        print(cleaned_text)
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use image path from command line argument
        image_path = sys.argv[1]
    else:
        # Prompt for image path
        image_path = input("Enter the path to the image file: ").strip()
    
    test_ocr(image_path)

