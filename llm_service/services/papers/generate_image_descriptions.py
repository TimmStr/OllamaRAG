import base64
import os
import re
from io import BytesIO

from PIL import Image

from entities.ollama_entities import QwenVision
from services.papers.edit_headlines import gen_text_docs
from utils import get_erp_image_paths
from utils.logging_config import exception_handling
from utils.paths import PAPERS_OUTPUT_IMAGES


@exception_handling
def convert_to_base64(pil_image):
    """
    Convert PIL images to Base64 encoded strings
    :param pil_image: PIL image
    :return: Base64 string
    """
    try:
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    except:
        return ""


def get_header_description(headers_for_page):
    if len(headers_for_page) < 2:
        return f"Die Überschrift für das Kapitel in dem das Bild stand lautet: {headers_for_page[0]}.\n"
    return f"Die Überschrift für das Kapitel in dem das Bild stand ist in folgendem Array enthalten. Vielleicht hilft dir das bei der Beschreibung: {headers_for_page}.\n"


def write_description_to_file(description, img_path):
    with open(os.path.join(PAPERS_OUTPUT_IMAGES, "descriptions",
                           os.path.basename(img_path).split(".")[0] + ".txt"), "w+") as f:
        f.write(description)


@exception_handling
def generate_paper_image_descriptions():
    qwen_llm = QwenVision().create()
    header_pages_dict = {doc.page_content.splitlines()[0]: doc.metadata["pages"] for doc in gen_text_docs()}

    for img_path in get_erp_image_paths():
        try:
            page_number = re.search(r'\d+', os.path.basename(img_path)).group()

            headers_for_page = [header for header, page_numbers in header_pages_dict.items() if
                                int(page_number) in page_numbers]

            llm_with_image_context = qwen_llm.bind(images=[convert_to_base64(Image.open(img_path))])

            description = llm_with_image_context.invoke(
                f"Bitte gib mir eine kurze Beschreibung für das Beispielbild. Halte dich also kurz und prägnant und erkläre nur Dinge die du siehst, wie zum Beispiel die Menüüberschrift und Unterpunkte. {get_header_description(headers_for_page)}:")
            write_description_to_file(description, img_path)
        except:
            print("Failed for:", img_path)


if __name__ == "__main__":
    generate_paper_image_descriptions()
