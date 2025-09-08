import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import re
import os

class OCREngine:
    """OCR engine for extracting text from financial documents"""
    
    def __init__(self, tesseract_path=None):
        # Configure Tesseract path
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            # Try to auto-detect Tesseract path
            try:
                # Common paths for different OS
                if os.name == 'nt':  # Windows
                    possible_paths = [
                        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
                    ]
                else:  # Linux/Mac
                    possible_paths = ['/usr/bin/tesseract', '/usr/local/bin/tesseract']
                
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
                else:
                    print("Warning: Tesseract not found. Please install Tesseract OCR")
            except Exception as e:
                print(f"Error configuring Tesseract: {e}")
    
    def preprocess_image(self, image):
        """Preprocess image to improve OCR accuracy"""
        try:
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Remove noise
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            processed = cv2.medianBlur(processed, 3)
            
            return processed
        except Exception as e:
            print(f"Error in image preprocessing: {e}")
            return image
    
    def extract_text(self, image_path=None, image_bytes=None):
        """Extract text from image using OCR"""
        try:
            # Load image
            if image_path:
                if not os.path.exists(image_path):
                    return {"error": f"Image path {image_path} does not exist", "success": False}
                image = cv2.imread(image_path)
                if image is None:
                    return {"error": f"Failed to load image from {image_path}", "success": False}
            elif image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    image = np.array(image)
                except Exception as e:
                    return {"error": f"Failed to process image bytes: {str(e)}", "success": False}
            else:
                return {"error": "No image provided", "success": False}
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Perform OCR with different configurations for better accuracy
            custom_configs = [
                r'--oem 3 --psm 6',  # Assume a single uniform block of text
                r'--oem 3 --psm 4',  # Assume a single column of text of variable sizes
                r'--oem 3 --psm 3',  # Fully automatic page segmentation, but no OSD
            ]
            
            results = {}
            for i, config in enumerate(custom_configs):
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    results[f"config_{i}"] = text
                except Exception as e:
                    print(f"OCR with config {config} failed: {e}")
            
            # Use the result with the most text (likely the most accurate)
            best_result = max(results.values(), key=len) if results else ""
            
            return {
                "raw_text": best_result,
                "all_results": results,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def detect_document_type(self, text):
        """Heuristic method to detect document type"""
        text_lower = text.lower()
        
        # Check for invoice keywords
        invoice_keywords = ['invoice', 'inv#', 'inv no', 'invoice no', 'bill to', 'ship to', 'invoice date']
        if any(keyword in text_lower for keyword in invoice_keywords):
            return "Invoice"
        
        # Check for quote keywords
        quote_keywords = ['quote', 'quotation', 'estimate', 'proposal', 'quote no']
        if any(keyword in text_lower for keyword in quote_keywords):
            return "Quote"
        
        # Check for receipt keywords
        receipt_keywords = ['receipt', 'payment received', 'thank you for your business', 'paid on']
        if any(keyword in text_lower for keyword in receipt_keywords):
            return "Receipt"
        
        # Check for bill keywords
        bill_keywords = ['bill', 'statement', 'amount due', 'due date', 'account summary']
        if any(keyword in text_lower for keyword in bill_keywords):
            return "Bill/Statement"
        
        return "Unknown"