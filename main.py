
import os
import sys
import argparse
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ocr.ocr_engine import OCREngine
from nlp.nlp_processor import NLPEngine
from sentiment.sentiment_analyzer import SentimentAnalyzer
from data_processing.data_processor import DataProcessor

class FinancialAIAnalyzer:
    """Main class for financial document analysis"""
    
    def __init__(self, tesseract_path=None):
        self.ocr_engine = OCREngine(tesseract_path)
        self.nlp_engine = NLPEngine()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.data_processor = DataProcessor()
    
    def process_document(self, image_path=None, image_bytes=None):
        """Process a financial document"""
        print("Starting document processing...")
        
        
        print("Performing OCR...")
        ocr_result = self.ocr_engine.extract_text(image_path, image_bytes)
        
        if not ocr_result.get("success", False):
            print(f"OCR failed: {ocr_result.get('error', 'Unknown error')}")
            return {"error": "OCR failed", "details": ocr_result.get("error", "Unknown error")}
        
        
        print("Detecting document type...")
        doc_type = self.ocr_engine.detect_document_type(ocr_result["raw_text"])
        
        
        print("Extracting entities with NLP...")
        nlp_entities = self.nlp_engine.extract_entities(ocr_result["raw_text"])
        
        
        print("Extracting financial data...")
        financial_data = self.nlp_engine.extract_financial_data(ocr_result["raw_text"])
        
        
        print("Analyzing sentiment...")
        sentiment = self.sentiment_analyzer.analyze_financial_sentiment(ocr_result["raw_text"])
        
        
        print("Structuring data...")
        structured_data = self.data_processor.structure_data(
            ocr_result, nlp_entities, financial_data, sentiment, doc_type
        )
        
        print("Document processing completed!")
        return structured_data

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Financial Document Analysis Tool')
    parser.add_argument('image_path', help='Path to the financial document image')
    parser.add_argument('--output', '-o', help='Output directory for results', default='./results')
    parser.add_argument('--tesseract', '-t', help='Path to Tesseract executable (if not in PATH)')
    
    args = parser.parse_args()
    
    
    if not os.path.exists(args.image_path):
        print(f"Error: File {args.image_path} does not exist")
        return
    
   
    os.makedirs(args.output, exist_ok=True)
    
    
    analyzer = FinancialAIAnalyzer(tesseract_path=args.tesseract)
    result = analyzer.process_document(image_path=args.image_path)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        if 'details' in result:
            print(f"Details: {result['details']}")
        return
    
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_type = result['metadata']['document_type'].replace('/', '_')
    base_filename = f"{doc_type}_{os.path.splitext(os.path.basename(args.image_path))[0]}"
    
    
    json_path, csv_path = analyzer.data_processor.save_to_file(
        result, args.output, base_filename
    )
    
    print(f"\nProcessing completed successfully!")
    print(f"Document type: {result['metadata']['document_type']}")
    
   
    if result['financial_data'].get('totals'):
        print(f"Total amounts: {', '.join(result['financial_data']['totals'])}")
    if result['financial_data'].get('taxes'):
        print(f"Tax amounts: {', '.join(result['financial_data']['taxes'])}")
    if result['financial_data'].get('ids'):
        print(f"Document IDs: {', '.join(result['financial_data']['ids'])}")
    
    print(f"Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
    print(f"Urgency: {result['sentiment'].get('urgency', 'LOW')}")

if __name__ == "__main__":
    main()