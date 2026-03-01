# src/parsers.py
import json
from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from src.config import config
from src.dependencies import get_llm

class BaseParser(ABC):
    """Abstract base class for document parsers supporting multiple modes and enrichment."""
    
    def __init__(self, mode: str = "large"):
        self.mode = mode.lower()
        
        # --- Granular Mode Tools ---
        # Splits strictly at every header to create many small context-specific chunks
        self.headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        self.md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=self.headers_to_split_on)
        self.granular_char_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
        # --- Large Mode Tools ---
        # Aimed at creating ~2 large chunks per file to keep tables/endpoints intact
        self.large_chunk_size = 4000
        self.large_chunk_overlap = 200

        # --- Enrichment Configuration ---
        # Toggles whether to call the LLM during the ingestion process
        self.use_llm_enrichment = config.get("ingestion", {}).get("enrich_metadata", False)
        if self.use_llm_enrichment:
            self.llm = get_llm()

    @abstractmethod
    def parse(self, file_path: str, base_metadata: dict) -> List[Document]:
        """Parses a file and returns a list of Document chunks."""
        pass

    def _enrich_with_llm(self, doc: Document) -> Document:
        """Internal helper to generate metadata (summary, keywords, questions) via LLM."""
        prompt = f"""
        Analyze the following API documentation chunk.
        Provide a JSON response with three keys:
        1. "summary": A 1-sentence summary of what this chunk explains.
        2. "keywords": A list of 3-5 technical keywords.
        3. "questions": A list of 2 hypothetical user questions this chunk perfectly answers.
        
        Chunk Content:
        {doc.page_content}
        
        Respond ONLY with valid JSON.
        """
        try:
            print(f"Enriching chunk via LLM...")
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            if content.startswith("```json"): content = content[7:-3]
            enrichment_data = json.loads(content)
            doc.metadata.update(enrichment_data)
        except Exception as e:
            print(f"Metadata enrichment failed: {e}")
        return doc

    def finalize_chunks(self, chunks: List[Document]) -> List[Document]:
        """Optionally applies LLM enrichment to a list of documents."""
        if not self.use_llm_enrichment:
            return chunks
        return [self._enrich_with_llm(chunk) for chunk in chunks]


class MarkdownParser(BaseParser):
    def parse(self, file_path: str, base_metadata: dict) -> List[Document]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if self.mode == "granular":
                header_splits = self.md_header_splitter.split_text(content)
                for split in header_splits:
                    split.metadata.update(base_metadata)
                chunks = self.granular_char_splitter.split_documents(header_splits)
            else:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.large_chunk_size,
                    chunk_overlap=self.large_chunk_overlap,
                    separators=["\n## ", "\n### ", "\n\n", "\n", " "]
                )
                texts = splitter.split_text(content)
                chunks = [Document(page_content=t, metadata=base_metadata.copy()) for t in texts]

            return self.finalize_chunks(chunks)
        except Exception as e:
            print(f"Failed to parse Markdown file {file_path}: {e}")
            return []


class RSTParser(BaseParser):
    def parse(self, file_path: str, base_metadata: dict) -> List[Document]:
        try:
            if self.mode == "granular":
                chunks = self._parse_granular_rst(file_path, base_metadata)
            else:
                chunks = self._parse_large_rst(file_path, base_metadata)
            return self.finalize_chunks(chunks)
        except Exception as e:
            print(f"Failed to parse RST file {file_path}: {e}")
            return []

    def _parse_large_rst(self, file_path: str, base_metadata: dict) -> List[Document]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.large_chunk_size,
            chunk_overlap=self.large_chunk_overlap,
            separators=["\n\n..", "\n\n", "\n", " "]
        )
        texts = splitter.split_text(content)
        return [Document(page_content=t, metadata=base_metadata.copy()) for t in texts]

    def _parse_granular_rst(self, file_path: str, base_metadata: dict) -> List[Document]:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        documents = []
        current_content = []
        current_headers = {"Header 1": None, "Header 2": None, "Header 3": None}

        for i, line in enumerate(lines):
            clean_line = line.rstrip()
            if i + 1 < len(lines):
                next_line = lines[i+1].rstrip()
                if next_line and set(next_line).issubset({'=', '-', '~'}) and len(next_line) >= len(clean_line) and len(clean_line) > 0:
                    if current_content and any(current_headers.values()):
                        meta = base_metadata.copy()
                        meta.update({k: v for k, v in current_headers.items() if v})
                        documents.append(Document(page_content="\n".join(current_content).strip(), metadata=meta))
                        current_content = []
                    
                    char = next_line[0]
                    lvl = "Header 1" if char == '=' else "Header 2" if char == '-' else "Header 3"
                    current_headers[lvl] = clean_line
                    if lvl == "Header 1": current_headers["Header 2"] = current_headers["Header 3"] = None
                    elif lvl == "Header 2": current_headers["Header 3"] = None
                    current_content.append(clean_line)
                    continue

            if clean_line and set(clean_line).issubset({'=', '-', '~'}) and i > 0 and len(clean_line) >= len(lines[i-1].rstrip()):
                continue
            current_content.append(clean_line)

        if current_content:
            meta = base_metadata.copy()
            meta.update({k: v for k, v in current_headers.items() if v})
            documents.append(Document(page_content="\n".join(current_content).strip(), metadata=meta))

        return self.granular_char_splitter.split_documents(documents)

class ParserFactory:
    @staticmethod
    def get_parser(format_type: str, mode: str = "large") -> BaseParser:
        fmt = format_type.lower()
        if fmt == 'md': return MarkdownParser(mode=mode)
        elif fmt == 'rst': return RSTParser(mode=mode)
        else: raise ValueError(f"Unsupported format: {format_type}")