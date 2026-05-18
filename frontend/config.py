import os

# Configuration settings for the preprocessing pipeline

# Contractions dictionary for expansion
CONTRACTIONS = {
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "didn't": "did not",
    "doesn't": "does not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "mightn't": "might not",
    "mustn't": "must not",
    "it's": "it is",
    "that's": "that is",
    "who's": "who is",
    "what's": "what is",
    "there's": "there is",
    "here's": "here is",
    "let's": "let us",
    "they're": "they are",
    "we're": "we are",
    "you're": "you are",
    "I'm": "I am",
    "I've": "I have",
    "you've": "you have",
    "we've": "we have",
    "they've": "they have",
    "I'll": "I will",
    "you'll": "you will",
    "he'll": "he will",
    "she'll": "she will",
    "we'll": "we will",
    "they'll": "they will",
    "I'd": "I would",
    "you'd": "you would",
    "he'd": "he would",
    "she'd": "she would",
    "we'd": "we would",
    "they'd": "they would",
}

# Custom stopwords suitable for social media / reviews
CUSTOM_STOPWORDS = {"rt", "via", "amp", "u", "ur"}
