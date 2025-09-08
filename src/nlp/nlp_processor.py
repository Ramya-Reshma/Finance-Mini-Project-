import re
from datetime import datetime
import dateutil.parser as parser

class NLPEngine:
    """NLP engine for extracting entities from financial text without spaCy dependency"""
    
    def __init__(self):
        print("Using regex-based NLP processing (no spaCy dependency)")
    
    def extract_entities(self, text):
        """Extract entities from text using regex patterns"""
        entities = {
            "dates": [],
            "organizations": [],
            "persons": [],
            "money": [],
            "quantities": [],
            "locations": [],
            "products": []
        }
        
        # Enhanced regex patterns for entity extraction
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
        
        money_patterns = [
            r'\$\d+\.?\d*',
            r'\d+\.?\d*\s*(?:USD|EUR|GBP|INR)'
        ]
        
        # Company/organization patterns
        org_patterns = [
            r'(?:inc|llc|corp|corporation|limited|ltd|company|co)\.?\s+([A-Z][a-zA-Z0-9\s&]+)',
            r'([A-Z][a-zA-Z0-9\s&]+)\s+(?:inc|llc|corp|corporation|limited|ltd|company|co)\.?',
            r'payee:\s*([^\n]+)',
            r'pay to:\s*([^\n]+)',
            r'from:\s*([^\n]+)',
            r'vendor:\s*([^\n]+)',
            r'client:\s*([^\n]+)'
        ]
        
        # Person name patterns
        person_patterns = [
            r'attention:\s*([^\n]+)',
            r'attn:\s*([^\n]+)',
            r'contact:\s*([^\n]+)',
            r'dear\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        # Extract dates
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["dates"].extend(matches)
        
        # Extract money
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["money"].extend(matches)
        
        # Extract organizations
        for pattern in org_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["organizations"].extend(matches)
        
        # Extract persons
        for pattern in person_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["persons"].extend(matches)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def extract_financial_data(self, text):
        """Extract financial-specific information"""
        # Patterns for common financial data
        total_patterns = [
            r'total.*?(\$\d+\.?\d*)', 
            r'amount.*?(\$\d+\.?\d*)',
            r'balance.*?(\$\d+\.?\d*)',
            r'due.*?(\$\d+\.?\d*)',
            r'grand total.*?(\$\d+\.?\d*)',
            r'subtotal.*?(\$\d+\.?\d*)',
            r'total.*?(\d+\.?\d*)\s*(?:USD|EUR|GBP|INR)',
            r'amount.*?(\d+\.?\d*)\s*(?:USD|EUR|GBP|INR)'
        ]
        
        tax_patterns = [
            r'tax.*?(\$\d+\.?\d*)',
            r'gst.*?(\$\d+\.?\d*)',
            r'vat.*?(\$\d+\.?\d*)',
            r'tax amount.*?(\$\d+\.?\d*)',
            r'tax.*?(\d+\.?\d*)\s*(?:USD|EUR|GBP|INR)'
        ]
        
        # Extract totals
        totals = []
        for pattern in total_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            totals.extend(matches)
        
        # Extract taxes
        taxes = []
        for pattern in tax_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            taxes.extend(matches)
        
        # Extract dates with more specific patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        # Extract invoice numbers, order numbers, etc.
        id_patterns = [
            r'invoice no\.?\s*[:#]?\s*([A-Z0-9-]+)',
            r'invoice #\s*([A-Z0-9-]+)',
            r'order no\.?\s*[:#]?\s*([A-Z0-9-]+)',
            r'order #\s*([A-Z0-9-]+)',
            r'id\s*[:#]?\s*([A-Z0-9-]+)',
            r'reference no\.?\s*[:#]?\s*([A-Z0-9-]+)'
        ]
        
        ids = []
        for pattern in id_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ids.extend(matches)
        
        return {
            "totals": list(set(totals)),
            "taxes": list(set(taxes)),
            "dates": list(set(dates)),
            "ids": list(set(ids))
        }