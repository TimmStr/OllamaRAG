import csv
import os
import xml.etree.ElementTree as ET
from typing import List, Dict
from xml.etree.ElementTree import Element

import requests

from utils import create_dir
from utils.paths import DATA

BASE_URL = "http://export.arxiv.org/api/query?"


def safe_find(entry: Element, tag: str, default: str = "") -> str:
    """
    Safely find a tag in the XML element and return its text or an empty string if not found.
    """
    element = entry.find(tag)
    return element.text if element is not None else default


def extract_paper_information(entry: Element) -> Dict:
    title = safe_find(entry, "{http://www.w3.org/2005/Atom}title")
    summary = safe_find(entry, "{http://www.w3.org/2005/Atom}summary")
    authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in
               entry.findall("{http://www.w3.org/2005/Atom}author")]
    published = safe_find(entry, "{http://www.w3.org/2005/Atom}published")
    paper_url = safe_find(entry, "{http://www.w3.org/2005/Atom}id")
    pdf_url = paper_url.replace("abs", "pdf") + ".pdf"

    return {
        'title': title,
        'summary': summary,
        'authors': ", ".join(authors),
        'published': published,
        'url': paper_url,
        'pdf_url': pdf_url
    }


def get_arxiv_papers(**kwargs) -> List[Dict[str, str]]:
    """
    Fetches a list of the most relevant AI papers from arXiv based on the search query.

    Args:
        search_query (str): The search query string for arXiv.
        max_results (int): The number of results to fetch (default is 100).
        start_index (int): The start index for pagination (default is 0).

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing paper information.
    """
    papers = []
    url = f"{BASE_URL}search_query={kwargs.get('search_query')}&start={kwargs.get('start_index')}&max_results={kwargs.get('max_results')}&sortBy=relevance&sortOrder=descending"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
        return papers

    for entry in ET.fromstring(response.text).findall("{http://www.w3.org/2005/Atom}entry"):
        papers.append(extract_paper_information(entry))
    return papers


def download_pdf(pdf_url: str, save_dir: str, paper_title: str):
    """
    Download the PDF from the given URL and save it to the specified directory.
    """
    filename = paper_title.replace(" ", "_").replace("/", "_") + ".pdf"
    try:
        create_dir(save_dir)
        # Convert the title to a valid file name (no special characters)

        file_path = os.path.join(save_dir, filename)

        # Download PDF-File
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Save PDF
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF saved: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdf_url}: {e}")
    return filename


def save_to_csv(papers: List[Dict], **kwargs):
    filename = kwargs.get("filename")
    keys = ['title', 'summary', 'authors', 'published', 'url', 'pdf_url', 'file_path']
    if not papers:
        print("No papers to save.")
        return

    with open(filename, 'w+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)
    print(f"{len(papers)} Papers successfully saved in {filename}.")


def fetch_and_save_top_100_papers(**kwargs):
    """
    Pipeline to retrieve top influential papers for a topic and save the PDFs.
    """
    print("Collect top 100 most influential AI-Papers...")
    ai_papers = get_arxiv_papers(search_query=kwargs.get("search_query", "cat:cs.AI"),
                                 max_results=kwargs.get("max_results", 100),
                                 start_index=kwargs.get("start_index", 0))

    if ai_papers:
        for paper in ai_papers:
            pdf_url = paper.get('pdf_url')
            paper_title = paper.get('title')
            if pdf_url:
                filename = download_pdf(pdf_url,
                             kwargs.get("save_dir", os.path.join(DATA, "pdfs")),
                             paper_title)
                save_to_csv(ai_papers, **kwargs)
            else:
                print(f"No PDF available for paper: {paper_title}")
    else:
        print("No papers found.")


if __name__ == "__main__":
    fetch_and_save_top_100_papers()
