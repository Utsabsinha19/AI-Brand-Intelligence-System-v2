import pandas as pd
import numpy as np
from typing import List
import logging

from .cleaner import TextCleaner
from .tokenizer import TextTokenizer
from .lemmatizer import AdvancedLemmatizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NLPPreprocessingPipeline:
    """
    Orchestrates Cleaning, Tokenization, and Lemmatization steps
    for production-ready data pipelines.
    """
    def __init__(self, cleaner_kwargs=None, tokenizer_kwargs=None, lemmatizer_kwargs=None):
        self.cleaner = TextCleaner(**(cleaner_kwargs or {}))
        self.tokenizer = TextTokenizer(**(tokenizer_kwargs or {}))
        self.lemmatizer = AdvancedLemmatizer(**(lemmatizer_kwargs or {}))
        
    def process_text(self, text: str) -> str:
        """Processes a single textual record."""
        try:
            if pd.isna(text):
                return ""
                
            # Clean Noise
            cleaned_text = self.cleaner.clean(str(text))
            
            # Tokenize & Eliminate Stop Words
            tokens = self.tokenizer.tokenize(cleaned_text)
            
            # Reform for Lemmatizer consumption
            text_for_lemma = " ".join(tokens)
            
            # Lemmatize
            return self.lemmatizer.lemmatize(text_for_lemma)
        except Exception as e:
            logging.error(f"Error processing text: {e}")
            return ""

    def process_batch(self, texts: List[str]) -> List[str]:
        return [self.process_text(text) for text in texts]

    def process_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """Applies sequence transformations horizontally to pandas DataFrames."""
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame.")
            
        df[f"cleaned_{text_column}"] = df[text_column].apply(self.process_text)
        return df
