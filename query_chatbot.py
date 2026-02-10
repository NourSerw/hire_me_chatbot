from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

# Initialize HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Load existing ChromaDB
vectordb = Chroma(
    persist_directory="./vector_db",  
    embedding_function=embeddings
)

llm = OllamaLLM(model="llama2")  # or "mistral", "phi", etc.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 7})
)

# Simple similarity search
query = "Who is Nour?"
results = vectordb.similarity_search(query, k=7)
#print(f"Top {len(results)} results for query: '{query}'")
response = qa_chain.invoke(query)
print(response)

# for doc in results:
#     print(doc.page_content)
#     print("---")

