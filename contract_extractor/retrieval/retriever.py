from contract_extractor.retrieval.embeddings import EmbeddingModel
from contract_extractor.retrieval.vector_index import VectorIndex


class HybridRetriever:
    """
    Combines embedding-based retrieval with possible future extensions
    (keyword-based search, or hybrid approaches).
    """

    def __init__(self, chunks):
        self.chunks = chunks
        self.embeddings = EmbeddingModel()
        self.vector_index = VectorIndex(self.embeddings.embedder)
        self.vector_index.build_index(texts = [c.text for c in chunks], page_number=[c.page_start for c in chunks])

    def retrieve(self, query, k=5):
        return self.vector_index.query(query, k=k)
