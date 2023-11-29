# NLP (Natural Language Processing) breakdown
According to this article: https://www.kdnuggets.com/2018/10/main-approaches-natural-language-processing-tasks.html

NLP approaches = 
* Rule-based (human-defined rules and patterns to look for)
* "Traditional" machine learning approaches (like probabilistic modeling, likelihood maximization, and linear classifiers. Notably, these are not neural network models)
* Neural Networks

NLP task types = 
* Text Classification Tasks (find meaning without caring about word order, to flag topics and characterize text)
* Word Sequence Tasks (goal = language modeling, word order matters)
* Text Meaning Tasks (goal = how do we represent meaning)
* Sequence to Sequence Tasks (e.g. summarization and simplification tasks)
* Dialog Systems
    * Goal-oriented dialog systems focus on being useful in a particular, restricted domain
    * Conversational dialog systems are concerned with being helpful or entertaining in a much more general context


According to this article: https://monkeylearn.com/blog/natural-language-processing-techniques/

The top 7 techniques Natural Language Processing (NLP) uses to extract data from text are:
* Sentiment Analysis
* Named Entity Recognition
* Summarization
* Topic Modeling
* Text Classification
* Keyword Extraction
* Lemmatization and stemming


According to this article: https://monkeylearn.com/blog/natural-language-processing-techniques/

Some basic NLP data processing/preparation techniques include:
* Bag of words model
* Tokenisation
* Stop word removal
* Stemming
* Lemmatisation


The area of NLP most useful for our project (new bias detector) is probably **sentiment analysis**

## Sentiment Analysis:
According to this article: https://monkeylearn.com/sentiment-analysis/

Sentiment analysis finds the polarity of a text (positive, negative, neutral) but it also goes beyond polarity to detect emotions, urgency, and intentions.

Popular types of sentiment analysis = 
* Graded or fine-grained (polarity categories that include different levels of positive and negative, e.g. 0-5 stars rating)
* Emotion detection
* Aspect-based
* Multilingual

Sentiment analysis algorithms fall into one of 3 buckets:
* Rule-based
    * human-crafted rules to help identify subjectivity, polarity, or the subject of an opinion
    * These rules may include various NLP techniques, such as: 
        * Stemming, tokenization, part-of-speech tagging and parsing
        * Lexicons (i.e. lists of words and expressions)
* Automatic
    * feature extraction = transform the text into input for AI algorithm = text vectorization
        * methods = bag-of-words or bag-of-ngrams https://www.quora.com/What-is-the-difference-between-bag-of-words-and-bag-of-n-grams 
        * TF-IDF
        * word-embedding https://ai.stackexchange.com/questions/17273/is-word-embedding-a-form-of-feature-extraction 
    * generate/train the ML model
    * make predictions/classifications by passing data into model
* Hybrid (combine manual rules with automatic ML techniques)

Classification Algorithms = 
* Naïve Bayes
* Linear Regression
* Support Vector Machines
* Deep Learning (neural networks)

more info about how to perform text classification with AI: https://monkeylearn.com/text-classification/





