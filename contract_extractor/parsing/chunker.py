from typing import List
from dataclasses import dataclass
from pathlib import Path
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# OUTPUT STRUCTURE
# -----------------------------
@dataclass
class Chunk:
    text: str
    page_start: int
    page_end: int
    section_title: str


# -----------------------------
# LEGAL PDF CHUNKER CLASS
# -----------------------------
class LegalPDFChunker:
    def __init__(
        self,
        chunk_size: int = 1500,
        chunk_overlap: int = 300,
    ):
        """
        Initialize legal PDF chunker with optimal defaults for contracts.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\nARTICLE ",
                "\n\nArticle ",
                "\n\nSECTION ",
                "\n\nSection ",
                "\n\n",
                "\n",
                ". ",
                " ",
            ],
        )

    # -----------------------------
    # SECTION TITLE EXTRACTOR
    # -----------------------------
    def _extract_section_title(self, text: str) -> str:
        """
        Extract probable legal section heading.
        """
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return ""

        first_line = lines[0]

        # ALL CAPS headings
        if re.match(r"^[A-Z\s\.\-\,]{5,}$", first_line):
            return first_line

        # Numbered clauses (1., 1.1, etc.)
        if re.match(r"^\d+(\.\d+)*\s+", first_line):
            return first_line

        # Default: first sentence
        return first_line[:200]

    # -----------------------------
    # MAIN METHOD
    # -----------------------------
    def chunk_pdf(self, pdf_path: str) -> List[Chunk]:
        """
        Chunk legal PDF into structured chunks.
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"{pdf_path} not found")

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        split_docs = self.splitter.split_documents(documents)

        chunks: List[Chunk] = []

        for doc in split_docs:
            text = doc.page_content.strip()
            page = doc.metadata.get("page", 0) + 1  # Convert to 1-indexed

            section_title = self._extract_section_title(text)

            chunks.append(
                Chunk(
                    text=text.strip().replace("\xa0", ' '),
                    page_start=page,
                    page_end=page,
                    section_title=section_title,
                )
            )

        return chunks