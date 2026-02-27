from langchain_community.vectorstores import FAISS

class VectorIndex:
    def __init__(self, embedding_model):
        self.index = None
        self.embedding_model = embedding_model

    def build_index(self, texts, page_number):
        metadata = [{"page_number": p} for p in page_number]
        self.index = FAISS.from_texts(
            texts,
            self.embedding_model,
            metadatas=metadata,            # ✅ pass object, not vectors
        )

    def query(self, query_text, k=5):
        results = self.index.similarity_search(query_text, k=k)
        # Return text + page number
        return [
            {
                "content": doc.page_content,
                "page_number": doc.metadata.get("page_number")
            }
            for doc in results
        ]
