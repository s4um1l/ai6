import os
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    print("ReportLab not installed. Install with 'pip install reportlab'")
    exit(1)

def create_sample_pdf(output_path="data/sample.pdf"):
    """Create a sample PDF file with some text for testing"""
    # Make sure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create a new PDF with Reportlab
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add a title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Sample PDF for RAG Testing")
    
    # Add a paragraph of text
    c.setFont("Helvetica", 12)
    
    text = """
    This is a sample PDF document created for testing the PDF loader functionality 
    in our enhanced RAG application. The PDFFileLoader class should be able to extract 
    this text and make it available for processing.
    
    The Michael Eisner Memorial Weak Executive Problem is a common issue in organizations
    where a CEO who previously excelled in a particular function tends to hire weak executives
    in that area so they can continue to be "the expert" in their original domain.
    
    This was named after Michael Eisner, the former CEO of Disney, who had been a brilliant
    TV network executive. When Disney acquired ABC under his leadership, the network fell
    to fourth place in ratings. Eisner's response was telling: "If I had an extra two days
    a week, I could turn around ABC myself."
    """
    
    # Split the text into multiple lines and draw on the PDF
    y_position = 730
    for line in text.strip().split('\n'):
        stripped_line = line.strip()
        if stripped_line:
            c.drawString(100, y_position, stripped_line)
            y_position -= 15
    
    # Add some content for page 2
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Page 2: More RAG Concepts")
    
    c.setFont("Helvetica", 12)
    more_text = """
    Retrieval Augmented Generation (RAG) combines the power of large language models
    with the ability to retrieve information from external knowledge sources.
    
    The key components of a RAG system are:
    1. Document storage
    2. Vector embeddings
    3. Similarity search
    4. Text generation
    5. Prompt engineering
    
    Our implementation adds the following enhancements:
    - Sentence-based text chunking
    - Euclidean distance for similarity measurement
    - Metadata filtering for more precise retrieval
    - PDF document support
    """
    
    y_position = 730
    for line in more_text.strip().split('\n'):
        stripped_line = line.strip()
        if stripped_line:
            c.drawString(100, y_position, stripped_line)
            y_position -= 15
    
    # Save the PDF
    c.save()
    print(f"Sample PDF created at {output_path}")

if __name__ == "__main__":
    create_sample_pdf() 