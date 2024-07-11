import argparse
import os
from PDFscanner import main as pdf_scanner_main

def main():
    parser = argparse.ArgumentParser(description='Procesar un archivo PDF.')
    parser.add_argument('pdf_path', type=str, help='Ruta del archivo PDF a procesar.')

    args = parser.parse_args()

    if os.path.isfile(args.pdf_path):
        text_by_page = pdf_scanner_main(args.pdf_path)
        for i, page_text in enumerate(text_by_page):
            print(f"Página {i+1}:")
            print(page_text)
            print("\n" + "-"*50 + "\n")
    else:
        print("La ruta proporcionada no es un archivo válido.")

if __name__ == "__main__":
    main()
