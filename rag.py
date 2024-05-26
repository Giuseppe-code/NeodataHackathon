# load required library
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain


import os

# set OpenAI key as the environmet variable
os.environ['OPENAI_API_KEY'] = 'sk-roj-1hEdSeKhuGDKLxI28n5YT3BlbkFJX2V2H8b9THGIcqjP11e6'

# Load the embedding and LLM model
embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(model_name = "gpt-3.5-turbo", max_tokens = 200)



