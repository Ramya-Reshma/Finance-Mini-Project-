import pandas as pd
import json
from datetime import datetime
import os
import csv

class DataProcessor:
    """Data processor for structuring and saving results"""
    
    def __init__(self):
        self.processed_data = []
    
    def structure_data(self, ocr_result, nlp_entities, financial_data, sentiment, doc_type):
        """Structure all extracted data into a consistent format"""
        # Get current timestamp
        processed_time = datetime.now().isoformat()
        
        # Create structured data
        structured_data = {
            "metadata": {
                "processing_time": processed_time,
                "document_type": doc_type,
                "success": ocr_result.get("success", False)
            },
            "text": {
                "raw_text": ocr_result.get("raw_text", ""),
                "detailed_text": ocr_result.get("detailed_text", "")
            },
            "entities": nlp_entities,
            "financial_data": financial_data,
            "sentiment": sentiment
        }
        
        # Add to processed data history
        self.processed_data.append(structured_data)
        
        return structured_data
    
    def to_dataframe(self, structured_data):
        """Convert structured data to pandas DataFrame for analysis"""
        # Flatten the data for DataFrame
        flat_data = {
            "document_type": structured_data["metadata"]["document_type"],
            "processing_time": structured_data["metadata"]["processing_time"],
            "total_amounts": ", ".join(structured_data["financial_data"].get("totals", [])),
            "tax_amounts": ", ".join(structured_data["financial_data"].get("taxes", [])),
            "dates": ", ".join(structured_data["financial_data"].get("dates", [])),
            "document_ids": ", ".join(structured_data["financial_data"].get("ids", [])),
            "organizations": ", ".join(structured_data["entities"].get("organizations", [])),
            "persons": ", ".join(structured_data["entities"].get("persons", [])),
            "locations": ", ".join(structured_data["entities"].get("locations", [])),
            "sentiment": structured_data["sentiment"].get("label", "NEUTRAL"),
            "sentiment_score": structured_data["sentiment"].get("score", 0.5),
            "urgency": structured_data["sentiment"].get("urgency", "LOW")
        }
        
        return pd.DataFrame([flat_data])
    
    def save_to_file(self, structured_data, output_dir, base_filename=None):
        """Save processed data to files"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_type = structured_data["metadata"]["document_type"].replace("/", "_")
        
        if base_filename:
            filename = f"{base_filename}_{timestamp}"
        else:
            filename = f"{doc_type}_{timestamp}"
        
        # Save as JSON
        json_path = os.path.join(output_dir, f"{filename}.json")
        with open(json_path, 'w') as f:
            json.dump(structured_data, f, indent=2)
        
        # Save as CSV
        df = self.to_dataframe(structured_data)
        csv_path = os.path.join(output_dir, f"{filename}.csv")
        df.to_csv(csv_path, index=False, quoting=csv.QUOTE_ALL)
        
        print(f"Data saved to:")
        print(f"- JSON: {json_path}")
        print(f"- CSV: {csv_path}")
        
    
    def generate_summary_report(self, output_dir):
        """Generate a summary report of all processed documents"""
        if not self.processed_data:
            print("No data to generate report")
            return
        
        # Create a summary DataFrame
        summary_data = []
        for data in self.processed_data:
            summary_data.append({
                "document_type": data["metadata"]["document_type"],
                "processing_time": data["metadata"]["processing_time"],
                "total_amount": data["financial_data"].get("totals", [""])[0] if data["financial_data"].get("totals") else "",
                "tax_amount": data["financial_data"].get("taxes", [""])[0] if data["financial_data"].get("taxes") else "",
                "date": data["financial_data"].get("dates", [""])[0] if data["financial_data"].get("dates") else "",
                "sentiment": data["sentiment"].get("label", "NEUTRAL"),
                "urgency": data["sentiment"].get("urgency", "LOW")
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Save summary
        summary_path = os.path.join(output_dir, "summary_report.csv")
        summary_df.to_csv(summary_path, index=False)
        
        print(f"Summary report saved to: {summary_path}")
        return summary_path