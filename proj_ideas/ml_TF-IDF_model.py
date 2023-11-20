import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load your dataset (still in progress)
# df = pd.read_csv('news_article_dataset.csv')
# Our 'text' is the column with news articles and 'label' is the bias label

# Text preprocessing (still in progress)
    # Preprocessing Steps:
        # - Lowercasing
        # - Removing punctuation
        # - Removing stopwords
        # - Stemming or Lemmatization
        
def preprocess_text(text):
    # still in progress
    return processed_text

# Apply preprocessing
df['processed_text'] = df['text'].apply(preprocess_text)


# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(df['processed_text'], df['label'], test_size=0.2, random_state=42)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=1000) # We tune max_features later on
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Choose a classifier (SVM Classifier)

# 1.SVM Classifier
# classifier = SVC(kernel='linear')

# 2.Random Forest Classifier
classifier = RandomForestClassifier()

# Training the model
classifier.fit(X_train_tfidf, y_train)

# Predictions
predictions = classifier.predict(X_test_tfidf)

# Evaluation
print(classification_report(y_test, predictions))

