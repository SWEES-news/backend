Major goals of AI Bias analysis
===============================

### Analyze article content for bias
  - given an article's content, analyze it for bias. This functionality is shown in [`basic.py`](./basic.py).
  - Compare article to others with similar content, based on a vector store of previously-analyzed news or additional information on bias.


### Things needed to integrate with the rest of the system

#### Web scraping: Read articles using URLs
Some options:
 - Web scraping with BeautifulSoup4 - fairly straightforward, at least for articles with full access.
 - [Web scraping with LangChain](https://python.langchain.com/docs/use_cases/web_scraping) - something to consider when looking for similar articles to compare with.

### Links
Analyzed in `basic.py`:
- [News story 1](https://apnews.com/article/salmon-dams-tribes-columbia-snake-river-biden-51408c120a2e2dc147e6b07fe01d3531): [article input](./test_article.txt) and [response](./test_response.md)
- [News story 2](https://thevirginiastar.com/news/mercedes-benz-walks-back-on-huge-electric-vehicle-commitment-amid-slowing-demand/VAStarStaff/2024/02/25/): [article input](./test_article_2.txt) and [response](./test_response_2.md)
