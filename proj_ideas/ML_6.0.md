# ML

## Two Approaches:
This week we decided to approach the AI requirements of our projects in two different ways. One to ues an already existing LLM architecture to train our model, which will be explained in  details in another file. Second is to create our own model and train it from the ground. For that purpose we took a look at an article published by MIT regarding the midia bias to get an idea of how we can approach this problem. This is the link to this article: <https://arxiv.org/abs/2109.00024>
***
We used this article to come up with the features below.
***

For the purpose of training our model we need to choose some keywords in the articles that we find online. Those words should have these features:

### 1. Relevance:
In order to be relevant to a topic, a phrase must not be a very common one that has ambiguous stand-alone meaning. For example, the phrase “social media” could be promoting social media pages, as in “Follow us on social media”, or referencing a social media site. For simplicity, such common phrases with multiple meanings should be excluded.

A phrase is allowed to occur in multiple topics (for example, “socialism” is relevant to both the Venezuela and Cuba topics), but a sub-topic is not. For example, phrases related to the sub-topic tech censorship in China should be excluded from both the tech censorship and China topics because they are relevant to both.
### 2. Uniqueness:
Many phrases might appear with different capitalizations or conjugations. we might need to include only one of the phrase variations and discard the others.
### 3. Specificity:
Phrases must be specific enough to stand alone. A phrase is deemed specific if the phrase could be interpreted without context or be overwhelmingly likely to pertain to the relevant topic.
### 4. Organize Subtopics
### 5. Edge cases