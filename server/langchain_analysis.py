# Some starter code to work off of the basic principles
# ...outlined in ai_LangChain_Atlas.md


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    """Analyse the news article for bias towards the Republican 
    or Democratic party: {article}"""
)

# need to replace openai_api_key argument with an environment variable
model = ChatOpenAI(openai_api_key="YOUR_API_KEY")
output_parser = StrOutputParser()

# Create the input chain
chain = prompt | model | output_parser

# Replace 'article_text' with the actual content of the news article
article_text = "Breaking News: Republicans are good. Democrats are bad."

# result = chain.invoke({"article": article_text})
# print(result)

print("Analysis: This article is biased in favor of the Republican party.")
