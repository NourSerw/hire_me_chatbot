from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from utils import HireMeChatbotUtils
from config.logger import setup_logger

class PopulateDatabase:
    def __init__(self):
        self.logger = setup_logger(__name__)

    def load_documents(self):
        self.logger.info("Loading PDFs and Markdown files from 'docs/' folder.")
        
        # Load PDF files
        pdf_loader = DirectoryLoader(
            "docs/", 
            glob="**/*.pdf", 
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        pdf_docs = pdf_loader.load()
        
        # Load Markdown files (using default TextLoader)
        md_loader = DirectoryLoader(
            "docs/",
            glob="**/*.md",
            show_progress=True
        )
        md_docs = md_loader.load()
        
        # Combine all documents
        documents = pdf_docs + md_docs
        
        self.logger.info(f"✓ Loaded {len(pdf_docs)} PDF pages and {len(md_docs)} Markdown files ({len(documents)} total)")
        return documents
    
    def chunk_documents(self, documents):
        self.logger.info("Chunking...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        self.logger.info(f"✓ Created {len(chunks)} chunks")
        return chunks
    
    def load_database(self, embeddings):
        self.logger.info("Loading existing database...")
        vectordb = Chroma(
            persist_directory="./vector_db",
            embedding_function=embeddings
        )
        return vectordb
    
    def add_new_chunks(self, vectordb, chunks):
        self.logger.info("Adding new files to database.")
        # Generate custom IDs for each chunk
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        vectordb.add_documents(chunks, ids=ids)
        return ids

if __name__ == "__main__":
    populator = PopulateDatabase()
    documents = populator.load_documents()
    chunks = populator.chunk_documents(documents)
    utils = HireMeChatbotUtils()
    embeddings = utils.load_embeddings()
    vectordb = populator.load_database(embeddings)
    ids = populator.add_new_chunks(vectordb, chunks)