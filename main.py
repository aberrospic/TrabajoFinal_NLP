import os

import AIcomm
from PDFscanner import main as pdf_scanner_main

def split_text_into_chunks(text, max_chars=2047):
    """
    Divide un texto largo en chunks más pequeños.
    
    Args:
        text (str): Texto a dividir.
        max_chars (int): Número máximo de caracteres por chunk. Por defecto 2047.
    
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

def main(pdf_path):
    """
    Función principal que procesa un archivo PDF y genera resúmenes utilizando IA.
    """
    # Verificar si el archivo existe
    if os.path.isfile(pdf_path):
        texts = ""
        # Extraer texto del PDF
        text_by_page = pdf_scanner_main(pdf_path)
        # Imprimir el texto de cada página y concatenarlo
        for i, page_text in enumerate(text_by_page):
            print(f"Página {i+1}:")
            print(page_text)
            texts += "\n"
            texts += page_text
            print("\n" + "-"*50 + "\n")
        
        # Dividir el texto en chunks    
        text_chunks = split_text_into_chunks(texts, max_chars=2047)   
            
        # Procesar cada chunk con la IA
        for text in text_chunks:
            user_input = "Hazme un resumen de este texto: "
            user_input += text
            if user_input.lower() in ["salir", "exit"]:
                break
            response = AIcomm.handle_conversation(user_input)
            if response:
                print("\nAsistente: " + response+"\n")
    else:
        print("La ruta proporcionada no es un archivo válido.")

if __name__ == "__main__":
    pdf_path = "segunda-guerra-mundial-1b.pdf"
    main(pdf_path)
