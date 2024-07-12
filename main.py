import argparse
import os
from PDFscanner import main as pdf_scanner_main
import AIcomm

def main():
    parser = argparse.ArgumentParser(description='Procesar un archivo PDF.')
    parser.add_argument('pdf_path', type=str, help='Ruta del archivo PDF a procesar.')

    args = parser.parse_args()

    if os.path.isfile(args.pdf_path):
        texts = []
        text_by_page = pdf_scanner_main(args.pdf_path)
        for i, page_text in enumerate(text_by_page):
            print(f"Página {i+1}:")
            print(page_text)
            texts.append(page_text)
            print("\n" + "-"*50 + "\n")
        
            
        for text in texts:
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
