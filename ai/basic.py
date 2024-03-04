# basic usage of langchain for example.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

MODEL = 'gpt-4-turbo-preview' # 128,000 token max

prompt_template = (
  'Hello! You are a bias-finding analyst who has been tasked with determining '
  'the biases of a given news article. Please provide insights on this article '
  'while keeping in mind types of bias that may be apparent:\n'
  # see bias-analysis.md
  ' - Selection Bias: This occurs when a news outlet selectively reports on certain events over others, which can shape public perception by highlighting some issues while ignoring others.\n'
  ' - Reporting Bias: It involves a partial presentation of facts, where some details are emphasized over others to support a specific viewpoint. This can also include the omission of key facts that might contradict the outlet\'s preferred narrative.\n'
  ' - Confirmation Bias: This is more about the audience than the news outlet, where people favor information that confirms their preexisting beliefs. However, media outlets can exploit this bias by catering content to what they believe their audience wants to see or hear.\n'
  ' - Bias by Headline: Sometimes headlines can be misleading or designed to elicit an emotional response, rather than accurately summarizing the content of the article.\n'
  ' - Bias by Placement: The prominence given to a story, such as front-page news versus a brief mention in the back, can indicate the outlet\'s priorities or biases.\n'
  ' - Source Bias: This refers to the reliance on sources that may have a vested interest in how the story is told. It\'s important to consider who is being quoted and why.\n'
  ' - Visual Bias: Images, videos, and even the layout of a story can influence how the information is perceived. Visual elements can be used to evoke emotions or subtly sway opinion.\n'
  ' - Language and Tone Bias: The choice of words, the tone of the article, and the use of loaded language can all reveal bias. Neutral reporting strives for objective language devoid of any insinuation or judgment.\n\n'

  # TODO in future: retrieve additional articles based on their analyses and similarity to the input text

  'Here is the news article to analyze, delimited by triple quotes ("""):\n\n'

  '"""{content}"""\n\n'

  'Your response:\n'
)

def analyze_content(texts : list[str]) -> list[str]:
  """
  separately analyzes each text for news bias.

  :param texts: the texts to analyze.

  returns responses: a list of analyses.
  """
  prompt = ChatPromptTemplate.from_template(prompt_template)
  model = ChatOpenAI(model=MODEL)
  chain = prompt | model | StrOutputParser()

  docs = [{'content': doc} for doc in texts]

  responses = chain.batch(docs)

  return responses

def main():
  """Example of how to analyze content."""
  content_1 = ''; content_2 = ''

  with open('ai/test_article.txt', 'r') as article:
    content_1 = article.read()
  
  with open('ai/test_article_2.txt', 'r') as article2:
    content_2 = article2.read()
  
  responses = analyze_content([content_1, content_2])

  with open('ai/test_response.md', 'w') as out:
    print(responses[0], file=out)

  with open('ai/test_response_2.md', 'w') as out:
    print(responses[1], file=out)

if __name__ == "__main__":
  main()