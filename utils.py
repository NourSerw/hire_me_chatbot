from langchain_huggingface import HuggingFaceEmbeddings

class HireMeChatbotUtils:
    def __init__(self):
        pass

    def load_embeddings(self):
        """
        Load HuggingFace embedding model

        Returns:
            HuggingFaceEmbeddings: The loaded embedding model
        """
        print("Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        return embeddings