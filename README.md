

News Bias Tool
=============
The goal of this project is to make it easier to digest news articles and find biases within them. Our plan is to use a vector database to store articles scraped from the web and posted by users for analysis, then use a large language model (LLM) like ChatGPT to analyze the articles' biases.

**Problem:** There are many different reporters and organizations reporting news, and it is impossible for one person to research each one. It is also impossible for news reporting to be 100% objective since reporters have to choose what details to include in their stories and frame the story in a way that keeps readers interested. Given all this, how can a person catch the biases that inform each news report they consume?

**Solution:** Build a tool that will find all the articles/reports for a given story, analyze the differences between the articles, and use AI to detect the potential biases for each story. When a consumer reads a news article, they can use the tool analyze "between the lines" of the article and get a sense of how biased/objective that article may be.
### target customers
People who read news articles, and wish for ease in handling the complexities of news intake.
### implementation
###### tl;dr:
- scrape all the news
- store in vector database
- analyze bias with LLM
###### long form:
1. For this idea we'll need to scrape web data to find the publicly available articles on a specific topic to compare against the article the user wants to analyze.
2. We can use a vector database to store article content. This will store the relationships/similarities between articles. We can update this database with articles users upload (that they want to analyze) and articles scraped from the web. Doing so will update existing relationships in the database. Out-of-date articles can also be updated.
3. We will use a large language model (LLM, e.g. ChatGPT) to process an article and detect biases (and possibly find misinformation or opinionated judgements in the article). We may also keep track of media scores to deepen the model's understanding of what content is biased and in what direction.
4. We will have API endpoints to interact with the database and return the bias analysis on a given article.

### future work
These are things we will consider but are out of the scope of our solution...for this semester, at least ;)
- prioritize a user-friendly interface
- include a search tool to find news articles from our site
### potential problems
- We will be accessing so much data. It's hard to parse it all correctly and find the best way to store it.
- We may not have enough information on a topic stored - this has the potential of spreading misinformation.
- how to prevent hallucinations?
- properly analyzing news sources with context
- how to know what's biased, and what ways it's biased?
	- needs research
- dealing with vector databases

### competitors
- [Ground News](https://ground.news/)
- [AllSides](https://www.allsides.com/)
- [The Dispatch](https://thedispatch.com/) - right-leaning
- [News facts network](https://newsfactsnetwork.com/) - left-center leaning

---
## resources
<details>
<summary>Web scraping</summary>
<ul>
<li><a href="https://realpython.com/python-web-scraping-practical-introduction/">A practical introduction to web scraping in Python</a></li>
<li><a href="https://www.geeksforgeeks.org/python-web-scraping-tutorial/#">GeeksforGeeks: Web scraping tutorial</a></li>
<li><a href="https://www.newscatcherapi.com/blog/python-web-scraping-libraries-to-mine-news-data">NewsCatcher: 4 Python web scraping libraries for news data</a></li>
</ul>
</details>
<details>
<summary>LangChain and vector databases</summary>

> [Langchain tutorials in Python](https://python.langchain.com/docs/additional_resources/tutorials)
> [DeepLearning.AI Course - LangChain for LLM Application Development](https://learn.deeplearning.ai/langchain/)
> [DeepLearning.AI Course - LangChain: Chat with your Data](https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction)
</details>
<details markdown="1">
<summary>Our documentation</summary>

> [Writing Markdown on GitHub](https://docs.github.com/en/contributing)
</details>
