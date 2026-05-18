import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

for resource in ['wordnet', 'omw-1.4', 'averaged_perceptron_tagger']:
    try:
        nltk.data.find(f'corpora/{resource}' if 'tagger' not in resource else f'taggers/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

class AdvancedLemmatizer:
    def __init__(self, backend='spacy', model='en_core_web_sm'):
        self.backend = backend
        if self.backend == 'spacy':
            try:
                self.nlp = spacy.load(model, disable=['parser', 'ner'])
            except OSError:
                import subprocess
                import sys
                subprocess.run([sys.executable, "-m", "spacy", "download", model])
                self.nlp = spacy.load(model, disable=['parser', 'ner'])
        elif self.backend == 'nltk':
            self.lemmatizer = WordNetLemmatizer()
        else:
            raise ValueError("Unsupported backend. Use 'spacy' or 'nltk'.")

    def _get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts."""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def lemmatize(self, text: str) -> str:
        if not text:
            return ""
            
        if self.backend == 'spacy':
            doc = self.nlp(text)
            return " ".join([token.lemma_ for token in doc])
        else:
            tokens = text.split()
            return " ".join([self.lemmatizer.lemmatize(w, self._get_wordnet_pos(w)) for w in tokens])
