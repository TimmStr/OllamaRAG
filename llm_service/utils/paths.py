import os

DATA = "data"

CONFLUENCE_HTML_PAGES = os.path.join(DATA, "confluence_html_pages")

PAPERS = os.path.join(DATA, "papers")
PAPERS_OUTPUT = os.path.join(PAPERS, "output")
PAPERS_OUTPUT_IMAGES = os.path.join(PAPERS_OUTPUT, "images")
PAPERS_OUTPUT_IMAGE_DESCRIPTIONS = os.path.join(PAPERS_OUTPUT_IMAGES, "descriptions")

FAISS_INDICES = os.path.join(DATA, "faiss_indices")

FAISS_CONFLUENCE_TEXTS_IDX_FOLDER = os.path.join(FAISS_INDICES, "confluence_texts")
FAISS_CONFLUENCE_TEXTS_IDX_FILE = os.path.join(FAISS_CONFLUENCE_TEXTS_IDX_FOLDER, "index.faiss")

FAISS_ERP_IMG_DESC_IDX_FOLDER = os.path.join(FAISS_INDICES, "erp_image_descriptions")
FAISS_ERP_IMG_DESC_IDX_FILE = os.path.join(FAISS_ERP_IMG_DESC_IDX_FOLDER, "index.faiss")

FAISS_ERP_TEXT_IDX_FOLDER = os.path.join(FAISS_INDICES, "erp_texts")
FAISS_ERP_TEXT_IDX_FILE = os.path.join(FAISS_ERP_TEXT_IDX_FOLDER, "index.faiss")

FAISS_PAPERS_TEXTS_IDX_FOLDER = os.path.join(FAISS_INDICES, "papers")
FAISS_PAPERS_TEXTS_IDX_FILE = os.path.join(FAISS_PAPERS_TEXTS_IDX_FOLDER, "index.faiss")
