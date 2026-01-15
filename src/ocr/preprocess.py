from PIL import Image, ImageOps, ImageFilter
import numpy as np


def preprocess_image(path):
    """
    Load an image from disk and apply light preprocessing to improve OCR:
    - convert to grayscale
    - enhance contrast
    - apply sharpening
    - apply simple global thresholding to get a clean binary image

    Returns a NumPy array that can be passed directly to
    `pytesseract.image_to_string(Image.fromarray(...))`, matching the
    previous OpenCV-based behavior.
    """
    # Open image and convert to grayscale
    img = Image.open(path).convert("L")

    # Improve contrast
    img = ImageOps.autocontrast(img)

    # Slight sharpening to help OCR pick up strokes
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Simple global thresholding similar to the original logic
    threshold = 150
    img = img.point(lambda x: 255 if x > threshold else 0, mode="L")

    # Return as NumPy array to preserve the original API expectations
    return np.array(img)
