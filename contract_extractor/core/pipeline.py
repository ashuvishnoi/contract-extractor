from contract_extractor.parsing.chunker import LegalPDFChunker
from contract_extractor.retrieval.retriever import HybridRetriever
from contract_extractor.qa.qa_model import CUADQAModel
from contract_extractor.processing.postprocess import ValuesExtractor


class ExtractionPipeline:
    """Orchestrates parsing, retrieval, QA, and post-processing."""

    def __init__(self):
        self.chunker = LegalPDFChunker()
        self.qa_model = CUADQAModel()
        self.values_extractor = ValuesExtractor()

    def run(self, pdf, query, output_type):

        chunks = self.chunker.chunk_pdf(pdf)

        retriever = HybridRetriever(chunks)
        docs = retriever.retrieve(query, k=4)

        answer = self.qa_model.predict(query, docs, output_type)
        final_answer, page_number, snippet, confidence_score = self.values_extractor.value_extractor(value=answer, docs=docs)

        return {
            "value": final_answer,
            "found": answer is not None,
            "sources": [{"page": page_number, "snippet": snippet}] if docs else [],
            "confidence_score": confidence_score,
        }
