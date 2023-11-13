# More ML:
## 1. Feature Extraction with TF-IDF:
### Term Frequency (TF): 
This measures how frequently a term occurs in a document. In the TF calculation, all terms are considered equally important. However, in reality, certain terms, like stop words (e.g., "the", "is", "at"), may appear frequently but have little importance. Thus, simply counting terms can be misleading.
### Inverse Document Frequency (IDF):
This measures how important a term is within the entire corpus (the collection of all documents). It helps in diminishing the weight of terms that occur very frequently across documents and increases the weight of terms that occur rarely.

The TF-IDF value of a word in a document is the product of its TF and IDF scores. A high TF-IDF score indicates a term is more important to the document. TF-IDF is used for feature extraction in text analysis to convert textual data into a structured, numerical format that machine learning algorithms can understand. It effectively captures the importance of words in context to their frequency across documents.
***
## 2. Machine Learning Classifiers
### SVM (Support Vector Machine):
Overview: SVM is a powerful and versatile supervised machine learning algorithm, particularly effective in high-dimensional spaces, like those created by TF-IDF.

Working Principle: It works by finding the best hyperplane that separates data points of different classes. The best hyperplane is the one that has the largest margin, i.e., the maximum distance between data points of both classes.

Advantages: SVM is effective in cases where the number of dimensions is greater than the number of samples, which is often the case in text classification.
### Random Forest:
Overview: Random Forest is an ensemble learning method, which operates by constructing multiple decision trees during training and outputs the mode of the classes (classification) of the individual trees.

Working Principle: It creates multiple decision trees on randomly selected data samples, gets prediction from each tree, and selects the best solution by means of voting. It also provides a pretty good indicator of the feature importance.

Advantages: It's robust to overfitting and is capable of handling a large number of features, making it suitable for text classification where feature space is large.
***
## Combining TF-IDF with SVM/Random Forest
After transforming the text data into a numerical format using TF-IDF, this structured data should be fed into classifiers like SVM or Random Forest. These classifiers learn to make predictions based on the features (TF-IDF scores) of the input data.

For this approach we can use the libraries down below:

```py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
```

## Supervised vs Unsupervised
### Supervised:
creating neural network resource: https://realpython.com/python-ai-neural-network/ 

We can use existing datasets with labeled data for the purposes of bias detection: 
- https://datasetsearch.research.google.com/search?query=Bias%20Detection&docid=L2cvMTFqc2RkY2M0aA%3D%3D
- https://www.kaggle.com/datasets/timospinde/babe-media-bias-annotations-by-experts
- https://zenodo.org/records/4625151


### Unsupervised:
Since finding training data that exactly fits our purpose is difficult, we may also choose to take an unsupervised AI approach: 
https://www.datacamp.com/blog/introduction-to-unsupervised-learning