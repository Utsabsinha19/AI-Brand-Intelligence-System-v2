import spacy
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from .config import CUSTOM_STOPWORDS

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class TextTokenizer:
    def __init__(self, remove_stopwords=True, use_spacy=False, model='en_core_web_sm'):
        self.remove_stopwords = remove_stopwords
        self.use_spacy = use_spacy
        
        self.stopwords = set(nltk_stopwords.words('english')).union(CUSTOM_STOPWORDS)
        
        if self.use_spacy:
            try:
                self.nlp = spacy.load(model, disable=['parser', 'ner'])
            except OSError:
                import subprocess
                import sys
                subprocess.run([sys.executable, "-m", "spacy", "download", model])
                self.nlp = spacy.load(model, disable=['parser', 'ner'])
            self.stopwords = self.stopwords.union(self.nlp.Defaults.stop_words)

    def tokenize(self, text: str) -> list:
        if not text:
            return []
            
        tokens = [token.text for token in self.nlp(text)] if self.use_spacy else nltk.word_tokenize(text)
            
        if self.remove_stopwords:
            tokens = [word for word in tokens if word.lower() not in self.stopwords]
            
        return tokens
