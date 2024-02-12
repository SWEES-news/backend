"""
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
"""

import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Define the set of stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Removing punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Removing stopwords and stemming/lemmatization
    processed_tokens = []
    lemmatizer = WordNetLemmatizer()  # or use PorterStemmer() if you prefer stemming
    for token in tokens:
        if token not in stop_words:
            # Lemmatize tokens (or you can replace this with stemming)
            token = lemmatizer.lemmatize(token)
            processed_tokens.append(token)
    
    # Re-join tokens into a single string
    processed_text = ' '.join(processed_tokens)
    return processed_text

