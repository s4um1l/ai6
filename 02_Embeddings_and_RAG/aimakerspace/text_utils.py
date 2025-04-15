import os
import re
from typing import List, Optional
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class PDFFileLoader:
    """Load text from PDF files"""
    def __init__(self, path: str):
        self.documents = []
        self.path = path
        if not PDF_SUPPORT:
            raise ImportError(
                "PyPDF2 is required to load PDF files. Install it with 'pip install PyPDF2'"
            )
    
    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".pdf"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .pdf file."
            )
    
    def load_file(self):
        """Extract text from a single PDF file"""
        text = ""
        with open(self.path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        if text.strip():  # Only add if we extracted actual text
            self.documents.append(text)
    
    def load_directory(self):
        """Extract text from all PDF files in a directory"""
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    text = ""
                    with open(file_path, "rb") as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                    if text.strip():  # Only add if we extracted actual text
                        self.documents.append(text)
    
    def load_documents(self):
        """Load PDF documents and return as a list of strings"""
        self.load()
        return self.documents


class TextSplitter:
    """Base class for text splitters"""
    def split(self, text: str) -> List[str]:
        raise NotImplementedError("Must implement split method")

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


class CharacterTextSplitter(TextSplitter):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks


class SentenceTextSplitter(TextSplitter):
    """A text splitter that splits text by sentences and groups them into chunks"""
    def __init__(
        self,
        max_sentences_per_chunk: int = 10,
        sentence_overlap: int = 2,
    ):
        assert (
            max_sentences_per_chunk > sentence_overlap
        ), "Max sentences per chunk must be greater than sentence overlap"

        self.max_sentences_per_chunk = max_sentences_per_chunk
        self.sentence_overlap = sentence_overlap

    def split(self, text: str) -> List[str]:
        # Simple sentence splitting - you might want a more sophisticated approach
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        for i in range(0, len(sentences), self.max_sentences_per_chunk - self.sentence_overlap):
            chunk_sentences = sentences[i:i + self.max_sentences_per_chunk]
            chunks.append(" ".join(chunk_sentences))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
