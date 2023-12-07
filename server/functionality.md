# Functionality Analysis for AI News Bias Detector:
***

**Goal:**
Highlight the functionality/use cases that we want our project server to be able to handle. We will highlight basic functionality 
points for the backend, as well as optional add-ons that we may implement down the line. This will help conceptually break down our 
project, and inform what endpoints to define for our server. This list is subject to change. 

**Server/Backend Functionality Ideas:**
1. User Registration and Authentication
    - Allowing users to create accounts and log in securely to access the tool
2. Article Scraping and Storage
    - Automatically scraping news articles from various sources and storing them in the database for analysis
3. User-Uploaded Articles
    - Allowing users to upload articles they want to analyze for biases and misinformation
4. Bias Analysis
    - Figure out metrics (qualitative vs quantitative?) to measure and categorize bias, return the results to user
5. Bias Analysis Justificiation + Evidence
    - Offering explanations for the detected bias results/scores, indicating specific sentences or passages contributing to the bias
6. Recording Media Organization/Author Bias History
    - Keeping track of the perceived political leaning of media outlets and using this information to contextualize bias analysis
7. Search and Filtering Information
    - Enabling users to search for articles by topic, source, or bias score, and apply various filters
8. User Profiles
    - Allowing users to create and manage profiles, save articles, customize their preferences, and track their analysis history
9. User Feedback and Reporting
    - Providing a mechanism for users to report potential biases or inaccuracies in analysis results
10. Integrating with ChatGPT
    - Need to exchange information chatGPT, how to programmatically query ChatGPT?
11. Integration with Fact-Checking Services
    - Integrating 3rd fact-checking services to identify and flag misleading or false information in articles
12. Offering Educational Resources
    - Directing users to 3rd party educational content on media literacy, critical thinking, and detecting biases in news. Maybe summarize what each of the sources has to offer?
13. Privacy Settings
    - Allowing users to control their data privacy preferences and account permissions
14. Basic Help and Support
    - Give mission, basic tool usage instructions, overview of how the analysis works + metrics used
    - Allow users to submit questions and browse ansers?
15. Content Validation
    - Implementing a system to validate user-contributed articles to prevent the spread of misinformation or misuse. If articles are very trustworthy (according to user feedback and other fact checking mechanisms), that can be noted in database and used to help influence bias detection in other articles. 

---------

**(13) Planned Endpoint To Implement:**

(Note: anything in parentheses isn't an endpoint)

* User creates new account
* User logs in to existing account
* User can modify/update account info
* User can delete entire account
* User submits link (for AI analysis)
* User submits article text snippet (basically a portion of the content of the article)
    * (let's automatically save any submitted article snippets or links to the user's account history)
* User fetches from account...
    * All the article links they have submitted in the past (since we track article history)
    * All the article snippets they have submitted in the past
* User can delete from account...
    * Specific snippet 
        * (how to implement this? Either through some kind of snippet ID, or by having user re-submit the entire snippet so
        that we can match it to an existing snippet in the DB)
    * Specific article link
    * Clear all article history
    * Clear all snippet history
* User can check today’s news from the newsapi, get a list of (5?) article links they can read and get analyized 
    * (makes our tool useful for users who want a quick analysis on the most up to date news articles without waiting for human analyses)



