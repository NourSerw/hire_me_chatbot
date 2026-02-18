from langchain_huggingface import HuggingFaceEmbeddings

from config.logger import setup_logger

class HireMeChatbotUtils:
    def __init__(self):
        self.logger = setup_logger(__name__)

    def load_embeddings(self):
        """
        Load HuggingFace embedding model

        Returns:
            HuggingFaceEmbeddings: The loaded embedding model
        """
        self.logger.info("Loading embedding model.")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        return embeddings