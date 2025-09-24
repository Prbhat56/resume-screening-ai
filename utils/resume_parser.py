import PyPDF2
from docx import Document
import io

def extract_text_from_file(uploaded_file):
    """Extract text from PDF or DOCX files"""
    
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text

def extract_text_from_docx(uploaded_file):
    """Extract text from DOCX file"""
    doc = Document(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text