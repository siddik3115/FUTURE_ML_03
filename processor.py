import re
import PyPDF2
from docx import Document
import io

def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(file_bytes):
    """Extract text from a DOCX file."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_txt(file_bytes):
    """Extract text from a TXT file."""
    try:
        return file_bytes.decode("utf-8")
    except Exception as e:
        return f"Error reading TXT: {e}"

def clean_text(text):
    """Clean text by removing special characters, punctuation, and extra whitespace."""
    # Convert to lowercase
    text = text.lower()
    # Remove newlines and tabs
    text = re.sub(r'[\n\t\r]', ' ', text)
    # Remove special characters but keep alphanumeric and common punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_resume(file_bytes, file_name):
    """Parse resume based on file extension."""
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif file_name.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    elif file_name.endswith('.txt'):
        return extract_text_from_txt(file_bytes)
    else:
        return "Unsupported file format"
