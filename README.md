

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
- analyze sentiment of a text

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
<!-- in details tags, dropdowns need a line between summary and body to render Markdown properly -->
<details>
<summary>Web scraping</summary>

+ [A practical introduction to web scraping in Python](https://realpython.com/python-web-scraping-practical-introduction/)
+ [GeeksforGeeks: Web scraping tutorial](https://www.geeksforgeeks.org/python-web-scraping-tutorial/#)
+ [NewsCatcher: 4 Python web scraping libraries for news data](https://www.newscatcherapi.com/blog/python-web-scraping-libraries-to-mine-news-data)
</details>
<details>
<summary>LangChain and vector databases</summary>

+ [Langchain tutorials in Python](https://python.langchain.com/docs/additional_resources/tutorials)
+ [DeepLearning.AI Course - LangChain for LLM Application Development](https://learn.deeplearning.ai/langchain/)
+ [DeepLearning.AI Course - LangChain: Chat with your Data](https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction)
</details>
<details markdown="1">
<summary>Our documentation</summary>

+ [Writing Markdown on GitHub](https://docs.github.com/en/contributing)
</details>
<details>
<summary>Flask</summary>

+ [flask-dev](https://readthedocs.org/projects/flask-dev/downloads/pdf/latest/)
+ [fileuploads](https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/)
+ [sqlite3](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/)
+ [mysql](https://dev.mysql.com/doc/mysql-tutorial-excerpt/5.7/en/example-auto-increment.html)
+ [flask.make_response](https://tedboy.github.io/flask/generated/flask.make_response.html)
+ [config db](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)
</details>

https://newsdata.io/blog/news-api-python-client/


## Steps to run
> [!NOTE]
> If you're running a python environment, ensure you have it activated. Also be sure to have your NewsData.io API key stored in the environment variable `NEWS_API_KEY`. To automate starting these, you can run `source act.sh` if you have an existing virtual environment at the root named `.venv` and your API key is stored in a file named `.env` based on `.env.example`. For more information on NewsData.io, see [API Setup](#api-setup).


1. Run `make dev_env`.
2. Run `make tests`.
3. Run `./local.sh`.
4. Run `make prod`.
5. Run the menu: `dev.sh`.


## API Setup
### Set Environment Variable:
- [Get API Key](https://newsdata.io/api-key)
- **On macOS or Linux**:
    1. Open your terminal.
    2. Run the following command to set an environment variable (replace `YOUR_API_KEY` with the actual API key):
    ```bash
    export NEWS_API_KEY="YOUR_API_KEY"
    ```

- **On Windows**:
    1. Press `Win + X` and select "System".
    2. Click on "Advanced system settings" on the left.
    3. Click on "Environment Variables".
    4. Under "System variables", click "New" and enter `NEWS_API_KEY` as the variable name and your actual API key as the variable value.
- It's important to ensure that the environment variable is set every time you run your Python script. You might want to add the export command to your shell's profile script (e.g., ~/.bash_profile or ~/.zshrc on macOS and Linux) to ensure the environment variable is set automatically whenever you open a new terminal window.
- Future notes/plans
	- For a more permanent and portable solution, you might want to consider using a configuration file or a more advanced secret management solution, especially in a production environment.


## Setting up MongoDB on MacOS

This section guides you through the process of installing MongoDB on MacOS using Homebrew and connecting to your MongoDB instance.

### Prerequisites

- MacOS with Homebrew installed.
- Terminal access.

### Installation Steps

1. **Add MongoDB Repository to Homebrew**:
   MongoDB provides a custom Homebrew tap. Adding this tap allows you to install MongoDB directly through Homebrew. Run the following command to add the MongoDB tap:
   ```
   brew tap mongodb/brew
   ```

2. **Install MongoDB Community Edition**:
   Once you have tapped the MongoDB repository, you can install MongoDB Community Edition using the following command:
   ```
   brew install mongodb-community
   ```

3. **Start the MongoDB Service**:
   After installation, you can start the MongoDB service. This will initiate the MongoDB server and make it ready for connections:
   ```
   brew services start mongodb-community
   ```

4. **Connecting to MongoDB**:
   - **Using `mongosh` (Recommended)**: Newer MongoDB installations come with `mongosh`, the MongoDB Shell, as the default CLI tool for interaction. You can connect to your local MongoDB instance by simply typing:
     ```
     mongosh
     ```
   - **Using `mongo` (Legacy)**: In older versions or if you have `mongo` installed separately, you can connect using:
     ```
     mongo
     ```

### Verifying the Installation

To verify that MongoDB is running correctly, use the `mongosh` or `mongo` command to connect to your MongoDB instance. If you encounter any issues, ensure that MongoDB is correctly started and that there are no network or firewall configurations blocking the connection.

For detailed documentation and advanced configuration, refer to the [official MongoDB documentation](https://docs.mongodb.com/manual/).
