import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


MODEL = 'gpt-4-turbo-preview'  # 128,000 token max

PROMPT_TEMPLATE = (
    'Hello! You are a bias-finding analyst who has been tasked with '
    'determining the biases of a given news article. Please provide insights '
    'on this article while keeping in mind types of bias that may be '
    'apparent:\n'
    # see bias-analysis.md
    ' - Selection Bias: This occurs when a news outlet selectively reports on '
    'certain events over others, which can shape public perception by '
    'highlighting some issues while ignoring others.\n'
    ' - Reporting Bias: It involves a partial presentation of facts, where '
    'some details are emphasized over others to support a specific viewpoint. '
    'This can also include the omission of key facts that might contradict '
    'the outlet\'s preferred narrative.\n'
    ' - Confirmation Bias: This is more about the audience than the news '
    'outlet, where people favor information that confirms their preexisting '
    'beliefs. However, media outlets can exploit this bias by catering '
    'content to what they believe their audience wants to see or hear.\n'
    ' - Bias by Headline: Sometimes headlines can be misleading or designed '
    'to elicit an emotional response, rather than accurately summarizing the '
    'content of the article.\n'
    ' - Bias by Placement: The prominence given to a story, such as '
    'front-page news versus a brief mention in the back, can indicate the '
    'outlet\'s priorities or biases.\n'
    ' - Source Bias: This refers to the reliance on sources that may have a '
    'vested interest in how the story is told. It\'s important to consider '
    'who is being quoted and why.\n'
    ' - Visual Bias: Images, videos, and even the layout of a story can '
    'influence how the information is perceived. Visual elements can be used '
    'to evoke emotions or subtly sway opinion.\n'
    ' - Language and Tone Bias: The choice of words, the tone of the '
    'article, and the use of loaded language can all reveal bias. Neutral '
    'reporting strives for objective language devoid of any insinuation or '
    'judgment.\n\n'

    # TODO in future: retrieve additional articles based on
    # ...their analyses and similarity to the input text

    'Here is the news article to analyze, delimited by triple quotes ("""):'
    '\n\n"""{content}"""\n\n'
    'Your response:\n'
)


def create_vector_store(texts: list[str]) -> Chroma:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    try:
        splits = [text_splitter.split_text(doc) for doc in texts if doc]
        if not splits:
            logging.error("No valid splits were created from the provided texts.")
            return None
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        return vectorstore
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}")
        return None


def analyze_content(texts: list[str]) -> tuple[list[str], Chroma]:
    """
    Separately analyzes each text for news bias.

    :param texts: The texts to analyze.

    Returns responses: a list of analyses, and vectorstore: the Chroma vector store.
    """
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    model = ChatOpenAI(model=MODEL)
    chain = prompt | model | StrOutputParser()

    docs = [{'content': doc} for doc in texts]

    responses = chain.batch(docs)

    vectorstore = create_vector_store(texts)

    return responses, vectorstore


def read_content(file_path: str) -> str:
    """Reads content from a file and returns the content as a string.
    Returns None if there's an error reading the file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        logging.error(f"File not found {file_path}: {e}")
    except IOError as e:
        logging.error(f"IO error reading {file_path}: {e}")
    return None


def write_response(file_path: str, response: str):
    """Writes a response to a file."""
    try:
        with open(file_path, 'w') as file:
            print(response, file=file)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


def main():
    """Example of how to analyze content."""
    content_files = ['ai/test_article.txt', 'ai/test_article_2.txt']
    response_files = ['ai/test_response.md', 'ai/test_response_2.md']

    contents = [read_content(file) for file in content_files]
    responses, vectorDB = analyze_content(contents)

    query = "Any phrase that I want to check against the vectorDB"
    docs = vectorDB.similarity_search(query)
    print(docs[0].page_content)

    for response, file in zip(responses, response_files):
        write_response(file, response)


if __name__ == "__main__":
    main()
