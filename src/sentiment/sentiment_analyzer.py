from transformers import pipeline
import re

class SentimentAnalyzer:
    """Sentiment analyzer for financial text"""
    
    def __init__(self):
        try:
            self.analyzer = pipeline("sentiment-analysis")
        except Exception as e:
            print(f"Warning: Could not initialize transformer sentiment analyzer: {e}")
            print("Falling back to rule-based sentiment analysis only.")
            self.analyzer = None
    
    def analyze_text_sentiment(self, text):
        """Analyze sentiment of text"""
        if self.analyzer is not None:
            # For longer texts, we might need to chunk them
            if len(text) > 512:
                chunks = [text[i:i+512] for i in range(0, len(text), 512)]
                results = []
                for chunk in chunks:
                    try:
                        result = self.analyzer(chunk)[0]
                        results.append(result)
                    except:
                        continue
                
                if results:
                    # Aggregate results (simple approach)
                    positive_count = sum(1 for r in results if r['label'] == 'POSITIVE')
                    negative_count = sum(1 for r in results if r['label'] == 'NEGATIVE')
                    
                    if positive_count > negative_count:
                        return {"label": "POSITIVE", "score": positive_count/len(results)}
                    else:
                        return {"label": "NEGATIVE", "score": negative_count/len(results)}
                else:
                    return {"label": "NEUTRAL", "score": 0.5}
            else:
                try:
                    return self.analyzer(text)[0]
                except:
                    return {"label": "NEUTRAL", "score": 0.5}
        else:
            # Fallback to rule-based analysis if transformer is not available
            return self.analyze_financial_sentiment(text)
    
    def analyze_financial_sentiment(self, text):
        """Specialized sentiment analysis for financial context"""
        # Financial-specific keywords that might indicate positive/negative sentiment
        positive_keywords = [
            'discount', 'save', 'profit', 'gain', 'growth', 'positive',
            'benefit', 'advantage', 'success', 'approve', 'accept', 'thank you',
            'appreciate', 'valued customer', 'special offer', 'congratulations',
            'opportunity', 'pleasure', 'happy', 'satisfied'
        ]
        
        negative_keywords = [
            'due', 'overdue', 'penalty', 'late', 'charge', 'fee',
            'negative', 'loss', 'decline', 'reject', 'deny', 'outstanding',
            'past due', 'collection', 'termination', 'cancellation',
            'warning', 'problem', 'issue', 'error', 'sorry', 'apologize'
        ]
        
        urgent_keywords = [
            'urgent', 'immediate', 'asap', 'important', 'attention required',
            'final notice', 'action required'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        urgent_count = sum(1 for word in urgent_keywords if word in text_lower)
        
        # Determine overall sentiment
        if positive_count > negative_count:
            sentiment_label = "POSITIVE"
            sentiment_score = positive_count/(positive_count+negative_count+1)
        elif negative_count > positive_count:
            sentiment_label = "NEGATIVE"
            sentiment_score = negative_count/(positive_count+negative_count+1)
        else:
            sentiment_label = "NEUTRAL"
            sentiment_score = 0.5
        
        return {
            "label": sentiment_label,
            "score": sentiment_score,
            "urgency": "HIGH" if urgent_count > 0 else "LOW",
            "positive_keywords": positive_count,
            "negative_keywords": negative_count,
            "urgent_keywords": urgent_count
        }