# Importar las bibliotecas necesarias
import cv2
import numpy as np
import pymupdf
import pytesseract
from pdf2image import convert_from_path

# Configurar la ruta del ejecutable de Tesseract OCR si se ejecuta en Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def is_digitalized(pdf_path):
    """
    Determina si un PDF está digitalizado (contiene texto extraíble).
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
    
    Returns:
        bool: True si el PDF está digitalizado, False si no.
    """
    pdf_document = pymupdf.open(pdf_path)
    first_page = pdf_document.load_page(0)
    text = first_page.get_text()
    return bool(text.strip())

def extract_text_from_pdf(pdf_path):
    """
    Extrae texto de un PDF digitalizado.
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
    
    Returns:
        list: Lista de cadenas de texto, una por cada página del PDF.
    """
    pdf_document = pymupdf.open(pdf_path)
    num_pages = pdf_document.page_count
    text_by_page = []

    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        text_by_page.append(text)

    return text_by_page

def extract_text_from_image(image_path):
    """
    Extrae texto de una imagen utilizando OCR.
    
    Args:
        image_path (str): Ruta a la imagen o objeto de imagen.
    
    Returns:
        str: Texto extraído de la imagen.
    """
    text = pytesseract.image_to_string(image_path)
    return text

def convert_pdf_to_images(pdf_path):
    """
    Convierte un PDF en una lista de imágenes.
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
    
    Returns:
        list: Lista de objetos de imagen, uno por cada página del PDF.
    """
    images = convert_from_path(pdf_path)
    return images

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extrae texto de un PDF escaneado utilizando OCR.
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
    
    Returns:
        list: Lista de cadenas de texto, una por cada página del PDF.
    """
    images = convert_pdf_to_images(pdf_path)
    text_by_page = []

    for image in images:
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = extract_text_from_image(gray)
        text_by_page.append(text)

    return text_by_page

def main(pdf_path):
    """
    Función principal para extraer texto de un PDF, sea digitalizado o escaneado.
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
    
    Returns:
        list: Lista de cadenas de texto, una por cada página del PDF.
    """
    if is_digitalized(pdf_path):
        text_by_page = extract_text_from_pdf(pdf_path)
    else:
        text_by_page = extract_text_from_scanned_pdf(pdf_path)

    return text_by_page

def split_text_into_chunks(text, max_chars=2048):
    """
    Divide un texto largo en chunks más pequeños.
    
    Args:
        text (str): Texto a dividir.
        max_chars (int): Número máximo de caracteres por chunk.
    
    Returns:
        list: Lista de chunks de texto.
    """
    chunks = []
    start_idx = 0
    
    while start_idx < len(text):
        end_idx = start_idx + max_chars
        if end_idx < len(text):
            newline_pos = text.rfind('\n', start_idx, end_idx)
            if newline_pos != -1:
                end_idx = newline_pos + 1
        
        chunks.append(text[start_idx:end_idx])
        start_idx = end_idx
    
    return chunks

# Código de prueba (comentado)
'''
texts = []
pdf_path = "segunda-guerra-mundial-1b.pdf"
text_by_page = main(pdf_path)
for i, page_text in enumerate(text_by_page):
    print(f"Página {i+1}:")
    print(page_text)
    texts.append(page_text)
    print("\n" + "-"*50 + "\n")
    
text_chunks = split_text_into_chunks(texts, max_chars=1500)

chunks = []

for i, chunk in enumerate(text_chunks):
    print(f"Chunk {i+1}:")
    print(chunk)
    chunks.append(chunk)
    print("\n" + "-"*50 + "\n")
'''
