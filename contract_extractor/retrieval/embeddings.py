from langchain_huggingface import HuggingFaceEmbeddings
import os

HF_TOKEN = os.getenv("HF_TOKEN")


class EmbeddingModel:
    """Wrapper for sentence-transformer embeddings."""

    def __init__(self, model_path="gustavhartz/roberta-base-cuad-finetuned"):
        self.embedder = HuggingFaceEmbeddings(model_name=model_path, model_kwargs={
                "token": HF_TOKEN
            })

    def embed_documents(self, texts):
        return self.embedder.embed_documents(texts)
