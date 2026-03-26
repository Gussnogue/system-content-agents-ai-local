import PyPDF2
import docx
from PIL import Image
import io
import os

def extract_text_from_pdf(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {e}"

def extract_text_from_docx(file_bytes):
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Erro ao extrair texto do DOCX: {e}"

def extract_text_from_txt(file_bytes):
    try:
        return file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Erro ao extrair texto do TXT: {e}"

def extract_text_from_image(file_bytes, description=""):
    if description:
        return f"[Imagem] Descrição fornecida: {description}"
    else:
        return "[Imagem] Nenhuma descrição fornecida. A imagem foi armazenada, mas seu conteúdo não foi extraído."

def extract_text_from_file(uploaded_file, description=""):
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(file_bytes)
    elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return extract_text_from_image(file_bytes, description)
    else:
        return f"Formato não suportado: {filename}"
    
    