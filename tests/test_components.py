#!/usr/bin/env python3
"""
Test script for the Financial Document Analysis Tool
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocr.ocr_engine import OCREngine
from src.nlp.nlp_processor import NLPEngine
from src.sentiment.sentiment_analyzer import SentimentAnalyzer
from src.data_processing.data_processor import DataProcessor

def test_components():
    """Test individual components"""
    print("Testing OCR Engine...")
    ocr_engine = OCREngine()
    
    # Test with a simple image path (this will fail if no image exists, but we're testing the component initialization)
    try:
        result = ocr_engine.extract_text("non_existent_image.jpg")
        print("OCR Engine initialized successfully")
    except Exception as e:
        print(f"OCR Engine test failed: {e}")
    
    print("Testing NLP Engine...")
    try:
        nlp_engine = NLPEngine()
        print("NLP Engine initialized successfully")
        
        # Test entity extraction
        test_text = "Invoice dated 2023-01-15 from ABC Corp for $100.00"
        entities = nlp_engine.extract_entities(test_text)
        print(f"Entities extracted: {entities}")
        
    except Exception as e:
        print(f"NLP Engine test failed: {e}")
    
    print("Testing Sentiment Analyzer...")
    try:
        sentiment_analyzer = SentimentAnalyzer()
        print("Sentiment Analyzer initialized successfully")
        
        # Test sentiment analysis
        test_text = "Thank you for your payment. We appreciate your business."
        sentiment = sentiment_analyzer.analyze_financial_sentiment(test_text)
        print(f"Sentiment analysis: {sentiment}")
        
    except Exception as e:
        print(f"Sentiment Analyzer test failed: {e}")
    
    print("Testing Data Processor...")
    try:
        data_processor = DataProcessor()
        print("Data Processor initialized successfully")
    except Exception as e:
        print(f"Data Processor test failed: {e}")
    
    print("All components tested!")

if __name__ == "__main__":
    test_components()