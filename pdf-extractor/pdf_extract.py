import fitz

def extract(pdf):
    doc = fitz.open(pdf)
    return ''.join(page.get_text() for page in doc)

if __name__ == "__main__":
    print(extract("file.pdf"))