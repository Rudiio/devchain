from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
from pydantic import BaseModel

class SentimentAnalysisResult(BaseModel):
    negative: float
    positive: float
    
class SentimentAnalysis:
    def __init__(self):
        # Load the pre-trained RoBERTa model and tokenizer
        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.model = RobertaForSequenceClassification.from_pretrained('roberta-base')
        self.model.eval()  # Set the model to evaluation mode

    def preprocess(self, text):
        # Preprocess the input text for RoBERTa
        encoded_text = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
            return_tensors='pt',  # Return PyTorch tensors
            max_length=512,  # Truncate or pad to a length of 512 tokens
            padding='max_length',  # Pad to max_length
            truncation=True  # Truncate to max_length
        )
        return encoded_text

    def predict(self, preprocessed_text):
        # Predict the sentiment of the preprocessed text
        with torch.no_grad():  # Disable gradient calculation for inference
            outputs = self.model(**preprocessed_text)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return predictions

    def format_result(self, predictions):
        # Convert the model predictions to a user-friendly JSON response
        # Assuming the model has two labels: 0 (negative) and 1 (positive)
        sentiment_scores = predictions[0].tolist()  # Convert the first (and only) batch to a list
        sentiment_result = {
            'negative': sentiment_scores[0],
            'positive': sentiment_scores[1]
        }
        return sentiment_result

    def analyze(self, text):
        # Analyze the sentiment of the given text
        preprocessed_text = self.preprocess(text)
        predictions = self.predict(preprocessed_text)
        result = self.format_result(predictions)
        return result
