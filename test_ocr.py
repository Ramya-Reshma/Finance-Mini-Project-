import pytesseract
from PIL import Image
import os

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the path to your image file - using raw string format
image_path = r"C:\Users\RESHMA PARTHASARATHY\Downloads\sample_data.jpg"

# Check if file exists
if not os.path.isfile(image_path):
    print(f"ERROR: The file does not exist at {image_path}")
    print("Please check the path and try again.")
else:
    print("File found! Proceeding with OCR...")
    
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Perform OCR
        extracted_text = pytesseract.image_to_string(img)
        
        # Print the result
        print("\n--- EXTRACTED TEXT START ---\n")
        print(extracted_text)
        print("\n--- EXTRACTED TEXT END ---\n")
        
    except Exception as e:
        print(f"Error: {e}")