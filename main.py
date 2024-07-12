import argparse
import os
from PDFscanner import main as pdf_scanner_main
import AIcomm

def split_text_into_chunks(text, max_chars=2047):
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

def main():
    parser = argparse.ArgumentParser(description='Procesar un archivo PDF.')
    parser.add_argument('pdf_path', type=str, help='Ruta del archivo PDF a procesar.')

    args = parser.parse_args()

    if os.path.isfile(args.pdf_path):
        texts = ""
        text_by_page = pdf_scanner_main(args.pdf_path)
        for i, page_text in enumerate(text_by_page):
            print(f"Página {i+1}:")
            print(page_text)
            texts += "\n"
            texts += page_text
            print("\n" + "-"*50 + "\n")
        
        text_chunks = split_text_into_chunks(texts, max_chars=2047)   
            
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
    main()
