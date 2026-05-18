import re
from .utils import decode_html, expand_contractions, remove_emojis, fix_unicode

class TextCleaner:
    def __init__(self, lowercase=True, remove_url=True, remove_mentions=True, 
                 remove_html=True, remove_emoji=True, preserve_hashtags=True, 
                 normalize_stretched=True, remove_duplicates=True, expand_contract=True):
        self.lowercase = lowercase
        self.remove_url = remove_url
        self.remove_mentions = remove_mentions
        self.remove_html = remove_html
        self.remove_emoji = remove_emoji
        self.preserve_hashtags = preserve_hashtags
        self.normalize_stretched = normalize_stretched
        self.remove_duplicates = remove_duplicates
        self.expand_contract = expand_contract

    def clean(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        # 1. Unicode fix
        text = fix_unicode(text)
        
        # 2. HTML decoding and removal
        if self.remove_html:
            text = decode_html(text)
            text = re.sub(r'<[^>]+>', ' ', text)

        # 3. Lowercase
        if self.lowercase:
            text = text.lower()

        # 4. Expand Contractions
        if self.expand_contract:
            text = expand_contractions(text)

        # 5. Remove URLs
        if self.remove_url:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # 6. Remove Mentions
        if self.remove_mentions:
            text = re.sub(r'@\w+', '', text)

        # 7. Preserve Hashtags (strips '#' but keeps the word)
        if self.preserve_hashtags:
            text = re.sub(r'#(\w+)', r'\1', text)
        else:
            text = re.sub(r'#\w+', '', text)

        # 8. Remove Emojis
        if self.remove_emoji:
            text = remove_emojis(text)

        # 9. Normalize stretched words (e.g., soooo -> soo)
        if self.normalize_stretched:
            text = re.sub(r'(.)\1{2,}', r'\1\1', text)

        # 10. Remove punctuation & special characters (leaves whitespace & alphanumeric)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'[_]', ' ', text)
        
        # 11. Remove repetitive word patterns
        if self.remove_duplicates:
            text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)

        # 12. Remove unnecessary whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text
