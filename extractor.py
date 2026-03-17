import pytesseract
import cv2
import numpy as np
from PyPDF2 import PdfReader


def extract_text_from_file(filepath):
    text = ""
    try:
        if filepath.lower().endswith('.pdf'):
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() or ""
        else:
            # OpenCV loading with fallback for specialized characters
            image = cv2.imread(filepath)
            if image is None:
                return "Error: Could not read image file."

            # Simple Pre-processing to help Tesseract
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)

        return text.strip()
    except Exception as e:
        return f"Extraction Error: {str(e)}"
