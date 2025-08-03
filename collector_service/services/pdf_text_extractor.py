import os.path

from utils.paths import PDF_BASE_PATH

from pypdf import PdfReader


def extract_pdf_texts(path):
    reader = PdfReader(path)
    text = [page.extract_text() for page in reader.pages]
    return " ".join(text)


if __name__ == "__main__":
    print(extract_pdf_texts(os.path.join(PDF_BASE_PATH, "Active_Learning_with_Statistical_Models.pdf")))
