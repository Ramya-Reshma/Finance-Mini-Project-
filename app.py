from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import os
import cv2 # <-- NEW IMPORT
import numpy as np # <-- NEW IMPORT
import pytesseract

# Add this line with the correct path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# NEW FUNCTION: Add this function definition near the top
def preprocess_image(image_path):
    """
    Improve image quality for better OCR accuracy
    """
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply noise reduction
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to get black/white image
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save the processed image temporarily
    processed_path = "processed_image.jpg"
    cv2.imwrite(processed_path, thresh)
    
    return processed_path

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        f = request.files['file']
        # Save the file temporarily
        file_path = "uploads/" + f.filename
        f.save(file_path)
        
        # NEW: Preprocess the image before OCR
        processed_image_path = preprocess_image(file_path) # <-- ADD THIS LINE
        
        # MODIFIED: Use the preprocessed image for OCR
        img = Image.open(processed_image_path) # <-- CHANGE THIS LINE
        text = pytesseract.image_to_string(img)
        
        return render_template('result.html', extracted_text=text)

if __name__ == '__main__':
    app.run(debug=True)