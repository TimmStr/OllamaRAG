import os.path

from utils.paths import PDF_BASE_PATH, CSV_PATH

from pypdf import PdfReader
import csv


def extract_pdf_texts(path):
    reader = PdfReader(path)
    text = [page.extract_text() for page in reader.pages]
    return " ".join(text)


def extract_pdf_information(file_path):
    with open(CSV_PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[6] == file_path:
                return row
    return None


if __name__ == "__main__":
    print(extract_pdf_texts(os.path.join(PDF_BASE_PATH, "Active_Learning_with_Statistical_Models.pdf")))
