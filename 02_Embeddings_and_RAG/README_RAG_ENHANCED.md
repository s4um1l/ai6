# Enhanced RAG Application

This project enhances a basic Retrieval Augmented Generation (RAG) system with additional features, following SOLID principles to make minimal but impactful changes.

## New Features

### 1. Sentence-Based Text Chunking

We've added a new `SentenceTextSplitter` class that splits documents by sentences instead of characters:

```python
from aimakerspace.text_utils import SentenceTextSplitter

# Create a sentence splitter with 10 sentences per chunk and 2 sentences overlap
splitter = SentenceTextSplitter(max_sentences_per_chunk=10, sentence_overlap=2)
chunks = splitter.split_texts(documents)
```

This provides more semantic chunking compared to character-based splitting, as it preserves sentence boundaries.

### 2. Euclidean Distance Metric

We've added the Euclidean distance metric as an alternative to cosine similarity:

```python
from aimakerspace.vectordatabase import euclidean_distance

# Search using euclidean distance
results = vector_db.search_by_text(
    "What advice does Marc have about startups?", 
    k=3, 
    distance_measure=euclidean_distance
)
```

### 3. Metadata Filtering

We've added support for metadata filtering to allow more precise document retrieval:

```python
# Add metadata when building the vector database
metadata_list = [{"category": "startup"}, {"category": "career"}]
vector_db = await vector_db.abuild_from_list(chunks, metadata_list)

# Filter by metadata when searching
results = vector_db.search_by_text(
    "What advice does Marc have about startups?", 
    k=3,
    metadata_filter={"category": "startup"}
)
```

### 4. PDF File Support

We've added a `PDFFileLoader` class that can extract text from PDF files:

```python
from aimakerspace.text_utils import PDFFileLoader

# Load PDF documents
pdf_loader = PDFFileLoader("path/to/document.pdf")
documents = pdf_loader.load_documents()

# You can also load all PDFs in a directory
dir_loader = PDFFileLoader("path/to/pdf/directory")
all_pdf_documents = dir_loader.load_documents()

# Process the PDF content just like text documents
splitter = SentenceTextSplitter()
pdf_chunks = splitter.split_texts(documents)
```

Note: This requires the PyPDF2 library. Install it with `pip install PyPDF2`.

## Design Principles

The implementation follows these principles:

1. **Single Responsibility Principle**: Each class and function has a single responsibility
2. **Open-Closed Principle**: We extended functionality without modifying existing behavior
3. **Liskov Substitution Principle**: All text splitters inherit from a base class and can be used interchangeably
4. **Minimal Changes**: We made targeted changes to enhance functionality without restructuring

## Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API key set as environment variable
- PyPDF2 (for PDF support): `pip install PyPDF2`
- ReportLab (for sample PDF creation): `pip install reportlab`

### Installation

```bash
# Clone the repository
git clone [repository-url]

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key"
```

### Running the Demo

```bash
# Generate a sample PDF for testing (optional)
python create_sample_pdf.py

# Run the main demo
python test_rag_features.py
```

This will demonstrate all the new features:
- Compare character-based and sentence-based chunking
- Test PDF file loading (if a sample PDF is available)
- Compare cosine similarity and euclidean distance
- Demonstrate metadata filtering
- Run a complete RAG pipeline with the enhancements

## Implementation Details

### Text Splitting

We created a base `TextSplitter` class and made both `CharacterTextSplitter` and `SentenceTextSplitter` inherit from it, applying the Liskov Substitution Principle.

### Vector Database

We enhanced the `VectorDatabase` class to store metadata alongside vectors and added a filtering mechanism. The original API is preserved for backward compatibility.

### Distance Metrics

We implemented the euclidean distance as a standalone function, making it easy to swap distance metrics.

### PDF Support

We added a `PDFFileLoader` class that follows the same interface as the `TextFileLoader` but works with PDF files. It extracts text from each page and assembles it into documents.

## Next Steps

Potential future enhancements include:
- Add more sophisticated chunking strategies (e.g., paragraph-based, semantic-based)
- Implement more distance metrics
- Add support for more document types (HTML, DOCX, etc.)
- Improve metadata filtering with more complex queries
- Implement more advanced PDF text extraction with layout preservation 