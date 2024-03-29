# LangChain and MongoDB Atlas

### Description:
Using MongoDB Atlas Vector Search with Langchain's Retrieval-Augmented Generation (RAG) involves leveraging the strengths of both platforms to enhance the capabilities of Large Language Models (LLMs). MongoDB Atlas Vector Search allows for semantic similarity searches on your data, integrating with LLMs to build AI-powered applications. It supports storing and querying vector embeddings alongside your source data and metadata, facilitating fast semantic similarity searches using an approximate nearest neighbors algorithm.

LangChain is a framework designed to simplify the creation of LLM applications by providing a standard interface for chains, integrations with other tools, and end-to-end chains for common applications. This enables AI developers to build applications that leverage external data sources.

The RAG architecture helps overcome some limitations of LLMs, such as generating factually inaccurate information (hallucinations), dealing with stale data, and the lack of access to users' local data. RAG uses vector search to retrieve relevant documents based on an input query, providing these documents as context to the LLM to generate more informed and accurate responses.

To set up an environment for using Atlas Vector Search with Langchain RAG, you would typically start by installing necessary packages and creating Python scripts for loading your documents and enabling question-answering against your data using Atlas Vector Search and OpenAI.

For implementing LangChain RAG templates, you would install the langchain-cli and use it to bootstrap a LangServe project. This project would include a directory for LangServe code and another for your chains or agents, with modifications to the server.py file to incorporate the necessary code for your application.

MongoDB Atlas facilitates the creation of a vector search index in its UI, where you can configure fields of type vector for your embeddings. This setup allows for semantic searches on your Atlas cluster, supporting embeddings up to 2048 dimensions.

LangChain and OpenAI can be utilized together, with OpenAI providing vector embeddings and LangChain facilitating the development of applications that integrate these embeddings for richer, more personalized experiences.

### Istallation:

To install LangChain run:
```
pip install langchain-openai
```
The langchain-experimental package holds experimental LangChain code, intended for research and experimental uses. Install with:
```
pip install langchain-experimental
```
The LangChain CLI is useful for working with LangChain templates and other LangServe projects. Install with:
```
pip install langchain-cli
```
### LangSmith:
Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with LangSmith.
```
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="..."
```
### Quick Start:
Import the LangChain x OpenAI integration package.
```
pip install langchain-openai
```
Accessing the API requires an API key, which you can get by creating an OpenAI account and creating a key. Once we have a key we'll want to set it as an environment variable by running:
```
export OPENAI_API_KEY="..."
```
We can then initialize the model:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
```
A quick starter code base can be:
```python
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

# For demonstration, I'm using placeholders.
articles = [
    "This article discusses various policies implemented by the current administration...",
    "The recent legislation passed by the senate shows a clear bias towards...",
]

vectorstore = DocArrayInMemorySearch.from_texts(
    articles,
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

# We have to modify the template to analyze the political bias of the retrieved article.
template = """Analyze the political bias of the following article content:
{context}

Question: Does this article have a political bias towards Democrat, Republican, or show no clear bias?
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

# Chain setup to analyze bias.
chain = setup_and_retrieval | prompt | model | output_parser

# Invoke the chain with a query related to the article content to analyze its bias.
# The query can be a keyword or phrase from the article to retrieve it from the vector store.
bias_analysis_result = chain.invoke("current administration policies")

print(bias_analysis_result)

```

[Quickstart LangChain](https://python.langchain.com/docs/get_started/quickstart)  
[How to Perform Semantic Search Against Data in Your Atlas Cluster](https://www.mongodb.com/library/vector-search/how-to-perform-semantic-search?lb-mode=overlay)  
[MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search?utm_source=google&utm_campaign=search_gs_pl_evergreen_vector-stream_product_prosp-nbnon_gic-null_ww-multi_ps-all_desktop_eng_lead&utm_term=vector%20database&utm_medium=cpc_paid_search&utm_ad=p&utm_ad_campaign_id=20445624176&adgroup=155168612151&cq_cmp=20445624176&gad_source=1&gclid=CjwKCAiA8sauBhB3EiwAruTRJsTwl4pCMoqcCuLTjxzfQCzOw5qC9oWCTOH7WVNgB9pDoPyYAWh3DhoCCKQQAvD_BwE)  
[LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)
