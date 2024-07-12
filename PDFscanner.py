import cv2
import numpy as np
import pymupdf
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def is_digitalized(pdf_path):
    pdf_document = pymupdf.open(pdf_path)
    first_page = pdf_document.load_page(0)
    text = first_page.get_text()
    return bool(text.strip())

def extract_text_from_pdf(pdf_path):
    pdf_document = pymupdf.open(pdf_path)
    num_pages = pdf_document.page_count
    text_by_page = []

    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        text_by_page.append(text)

    return text_by_page

def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(image_path)
    return text

def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def extract_text_from_scanned_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    text_by_page = []

    for image in images:
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = extract_text_from_image(gray)
        text_by_page.append(text)

    return text_by_page

def main(pdf_path):
    if is_digitalized(pdf_path):
        text_by_page = extract_text_from_pdf(pdf_path)
    else:
        text_by_page = extract_text_from_scanned_pdf(pdf_path)

    return text_by_page

def split_text_into_chunks(text, max_chars=2048):
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

#Prueba
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
