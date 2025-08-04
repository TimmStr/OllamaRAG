import base64
import glob
import os
from typing import List, Dict

from natsort import natsorted

from utils.logging_config import exception_handling
from utils.paths import PAPERS_OUTPUT_IMAGES
from utils.paper_utils import extract_page_number_from_path


def bin_img_to_base64_dict(file_path: str) -> Dict:
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return {
            "filename": os.path.basename(file_path),
            "image_base64": f"data:image/png;base64,{encoded}"
        }


@exception_handling
def get_erp_images(pages: list) -> List:
    result = []
    for file_path in natsorted(glob.glob(os.path.join(PAPERS_OUTPUT_IMAGES, "p*"))):
        if int(extract_page_number_from_path(file_path)) in pages:
            result.append(bin_img_to_base64_dict(file_path))
    return result


@exception_handling
def image_from_path(paths: list) -> List:
    return [bin_img_to_base64_dict(img_path) for img_path in paths]
