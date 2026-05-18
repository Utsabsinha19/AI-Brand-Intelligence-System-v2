import re
import html
from .config import CONTRACTIONS

try:
    import emoji
    EMOJI_SUPPORT = True
except ImportError:
    EMOJI_SUPPORT = False

try:
    from langdetect import detect
    LANGDETECT_SUPPORT = True
except ImportError:
    LANGDETECT_SUPPORT = False

def decode_html(text: str) -> str:
    """Decodes HTML entities and tags."""
    return html.unescape(text)

def expand_contractions(text: str) -> str:
    """Expands contractions in the text using the config dictionary."""
    contractions_pattern = re.compile(
        '({})'.format('|'.join(CONTRACTIONS.keys())),
        flags=re.IGNORECASE | re.DOTALL
    )

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = CONTRACTIONS.get(match.lower(), match)
        if first_char.isupper():
            expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    # Handle floating single quotes
    expanded_text = re.sub(r"\'", "", expanded_text) 
    return expanded_text

def remove_emojis(text: str) -> str:
    """Removes emojis from text using emoji library or regex fallback."""
    if EMOJI_SUPPORT:
        return emoji.replace_emoji(text, replace='')
    else:
        # Regex fallback for emojis
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags (iOS)
            "\U00002702-\U000027b0"
            "\U000024c2-\U0001f251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

def fix_unicode(text: str) -> str:
    """Fixes common unicode errors by ignoring decoding faults."""
    return text.encode('utf-8', 'ignore').decode('utf-8')
