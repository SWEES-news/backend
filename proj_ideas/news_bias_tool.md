# Idea Analysis for Project:
***
## Idea 1: News Bias Detector Tool
### Description:
**Problem:**
There are many different reporters and organizations out there reporting news, and it is impossible for a person to research each one. 
It is impossible for news reporting to be 100% objective since reporters have to choose what details to include/omit in their 
stories, on top of figuring out how to frame the story to keep people interested. Given all this, how can a person catch all the biases that inform each news report they consume?
**Solutiuon:** 
Build a tool that will find all the articles/reports for a given story, analyze the differences between the articles, and use AI to 
detect the potential biases for each story. When a consumer reads a news article, they can use the tool analyze "between the lines" of 
the article and get a sense of how biased/objective that article may be. 
​
**Initial target customers:**
People that read news articles.
​
**Implementation:**
1. For this idea need to scrape web data to find the publicly available articles on a specific topic to compare against the article 
the user wants to analyze. 
2. We can have a database to store articles. We can store the relationshps/similarities between articles, and update this database 
with the articles users upload (that they want to analyze), articles scraped from the web, update existing relationships when another 
article on a given topic is uploaded, etc. Out-of-date articles can also be updated. 
3. Maybe group articles together by topic?
4. Use AI/ML to process an article and detect biases (and possibly any misinformation or opinionated judgements in the article).
5. Have different API endpoints to interact with the database and return the bias analysis on a given article. 
6. When new articles uploaded, we might choose to update any stored analysis/relationships of older articles on that topic already in the database.