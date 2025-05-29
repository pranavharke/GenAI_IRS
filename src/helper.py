# Importing Libraries
import os                                               # For interacting with the operating system 
from io import BytesIO                                  # To handle in-memory byte streams 
import pdfplumber                                       # To extract text from PDF files
from dotenv import load_dotenv                          # To load environment variables from a .env file
from langchain_groq import ChatGroq                     # LangChain interface to GROQ LLM API
from langchain_community.vectorstores import FAISS      # FAISS vector store integration from LangChain community repo
from langchain.memory import ConversationBufferMemory   # Memory module for conversational chains (chat history)
from langchain.chains import ConversationalRetrievalChain  # Chain combining retrieval and conversation for QA
from langchain_huggingface import HuggingFaceEmbeddings    # Embeddings from HuggingFace models for vectorization
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Splits large text into smaller chunks recursively
from langchain.prompts import PromptTemplate            # Template engine for custom LLM prompts
from langchain.schema import BaseRetriever, Document    # Base classes for document retrieval and document objects
from typing import List                                 # Type hinting for list types
from pydantic import PrivateAttr                        # Define private attributes in Pydantic models

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or ""

def get_pdf_text(pdf_file):
    """Extracts text from a PDF file and returns it as a string"""
    if not pdf_file:
        return ""

    try: # Ensure the file is seekable
        pdf_file.seek(0)
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e: # Handle any exceptions that occur during PDF reading
        return f"Error reading PDF: {e}"

def get_text_chunks(text):
    """Splits the input text into manageable chunks for processing"""
    # Use RecursiveCharacterTextSplitter to split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, metadatas):
    """Creates a vector store from the text chunks and their metadata"""
    # Ensure the text chunks and metadata are not empty
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embeddings, metadatas=metadatas)
    return vector_store

# This template is used to format the question and context for the LLM
QA_PROMPT = PromptTemplate( # Prompt template for question-answering
    template="""You are a helpful and knowledgeable assistant. Use the following context to answer the question as accurately, structured or semi-structured.  
                If the context is insufficient or unavailable, answer the question based on your general knowledge and information.  
                If a document source is available, then mention it. Always be formal, clear, and friendly in your response.

                {context} 
                Question: {question}
                Answer:""",
                input_variables=["context", "question"])

class MetadataPrependerRetriever(BaseRetriever):
    """A retriever that prepends metadata to the content of retrieved documents"""
    _base_retriever: BaseRetriever = PrivateAttr()  # Private attribute to hold the base retriever instance

    def __init__(self, base_retriever: BaseRetriever, **kwargs):
        """Initializes the MetadataPrependerRetriever with a base retriever"""
        super().__init__(**kwargs) 
        object.__setattr__(self, '_base_retriever', base_retriever)

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieves relevant documents and prepends metadata to their content"""
        docs = self._base_retriever.get_relevant_documents(query)
        for doc in docs: # Iterate through each document
            if "source" in doc.metadata: # If the document has a source in its metadata
                doc.page_content = f"[Source: {doc.metadata['source']}]\n{doc.page_content}"
        return docs

def get_conversational_chain(vector_store):
    """Creates a conversational retrieval chain using the provided vector store"""
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-70b-8192")                  # Initialize the LLM with Groq API key and model name
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)  # Initialize conversation memory to store chat history
    base_retriever = vector_store.as_retriever()                                        # Convert the vector store to a retriever
    wrapped_retriever = MetadataPrependerRetriever(base_retriever)                      # Wrap the base retriever to prepend metadata to retrieved documents

    chain = ConversationalRetrievalChain.from_llm( # Create a conversational retrieval chain
        llm, retriever=wrapped_retriever, memory=memory, combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return chain
