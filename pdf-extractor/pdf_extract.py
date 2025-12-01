import fitz
import os
from datetime import datetime

INPUT_FOLDER = "pdfs"
OUTPUT_FOLDER = "extracted_texts"
KEYWORDS = ["Python", "API"] 

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text(pdf_path, keywords=None):
    """Extracts text from a PDF, optionally filtering by keywords."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        page_count = len(doc)
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if keywords:
                if any(kw.lower() in text.lower() for kw in keywords):
                    full_text += f"\n--- Page {page_num} ---\n{text}"
            else:
                full_text += f"\n--- Page {page_num} ---\n{text}"
        word_count = len(full_text.split())
        return full_text, page_count, word_count
    except Exception as e:
        print(f"Failed to process {pdf_path}: {e}")
        return None, 0, 0

def process_folder(input_folder, output_folder, keywords=None):
    """Processes all PDFs in a folder."""
    summary = []
    for file in os.listdir(input_folder):
        if file.lower().endswith(".pdf"):
            path = os.path.join(input_folder, file)
            print(f"Extracting from {file}...")
            text, pages, words = extract_text(path, keywords)
            if text:
                output_file = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
                summary.append({
                    "file": file,
                    "pages": pages,
                    "words": words,
                    "saved_to": output_file,
                    "timestamp": datetime.now().isoformat()
                })
                print(f"Saved {output_file} ({pages} pages, {words} words)")
    return summary

if __name__ == "__main__":
    report = process_folder(INPUT_FOLDER, OUTPUT_FOLDER, keywords=KEYWORDS)
    print("\nSummary:")
    for entry in report:
        print(entry)
