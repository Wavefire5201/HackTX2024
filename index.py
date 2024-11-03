from langchain_core.messages import AIMessage
from langchain_iris import IRISVector
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
import os, dotenv
from Iris import Iris

dotenv.load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

llm = ChatOllama(model="llama3.1:8b", base_url=OLLAMA_HOST)
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url=OLLAMA_HOST)

irisLC = Iris(database=False)

loader = TextLoader("../data/state_of_the_union.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20)
docs = text_splitter.split_documents(documents)
