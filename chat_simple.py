import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 1. Cargar datos
loader = TextLoader("./datos.txt")
documents = loader.load()

print(documents)

# 2. Dividir texto
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

print(docs)
exit()

# 3. Embeddings (Usando DeepSeek)
embeddings = OpenAIEmbeddings(
    model="deepseek-embedding",
    openai_api_base="https://api.deepseek.com",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    check_embedding_ctx_length=False
)

# 4. Vector Store
vector = FAISS.from_documents(docs, embeddings)
retriever = vector.as_retriever()

# 5. Modelo LLM (DeepSeek)
llm = ChatOpenAI(
    model='deepseek-chat',
    temperature=0.1,
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com",
)

# 6. Chain
prompt = ChatPromptTemplate.from_template("""Responde la pregunta basándote solo en el siguiente contexto:
{context}

Pregunta: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# 7. Ejecutar
try:
    pregunta = "Que es RAG?"
    print(f"Pregunta: {pregunta}")
    response = retrieval_chain.invoke({"input": pregunta})
    print("Respuesta:", response["answer"])
except Exception as e:
    print(f"Error: {e}")