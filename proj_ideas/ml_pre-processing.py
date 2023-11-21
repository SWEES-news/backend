import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Downloads necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Converts text to lowercase
    text = text.lower()

    # Removes punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Removes stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in filtered_text]

    # Joins words into one string
    processed_text = ' '.join(stemmed_text)
    
    return processed_text
