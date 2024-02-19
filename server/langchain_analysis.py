# Some starter code to work off of the basic princples outlined to ai_LangChain_Atlas.md


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Analyse the news article for bias towards Republican or Democratic party: {article}")
model = ChatOpenAI(openai_api_key="YOUR_API_KEY")    # replace second arg with an environment variable
output_parser = StrOutputParser()

# Create the chain
chain = prompt | model | output_parser

# Replace 'article_text' with the actual content of the news article
article_text = "Breaking News: Republicans are good. Democrats are bad."

result = chain.invoke({"article": article_text})
print(result)