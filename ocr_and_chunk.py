from pdf2image import convert_from_path
import pytesseract
import re
import os

PDF_FILE = "HSC26-Bangla1st-Paper.pdf"
TEXT_FILE = "HSC26_Bangla_text.txt"
CHUNKS_FILE = "HSC26_Bangla_chunks.txt"

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text = "\n\n".join([pytesseract.image_to_string(p, lang="ben") for p in pages])
    return text

def split_into_chunks(text, max_len=500):
    sentences = [s.strip() for s in text.split("।") if s.strip()]
    chunks = []
    temp = ""
    for s in sentences:
        s += "।"
        if len(temp) + len(s) <= max_len:
            temp += s
        else:
            chunks.append(temp.strip())
            temp = s
    if temp:
        chunks.append(temp.strip())
    return chunks

def main():
    if not os.path.exists(TEXT_FILE):
        raw_text = extract_text_from_pdf(PDF_FILE)
        with open(TEXT_FILE, "w", encoding="utf-8") as f:
            f.write(raw_text)
    else:
        with open(TEXT_FILE, "r", encoding="utf-8") as f:
            raw_text = f.read()

    chunks = split_into_chunks(raw_text)
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(chunks))

    print(f"Extracted {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
