import os
from unittest.mock import patch, MagicMock

import pytest

from utils import mail_config, extract_page_number, remove_repeated_first_line, delete_repeating_lines_from_docs, \
    bin_images_to_text, get_erp_image_paths, get_erp_text_paths
from utils.constants import MAIL_USER, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT


@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        MAIL_HOST: "smtp.mailtrap.io",
        MAIL_USER: "user@example.com",
        MAIL_PASSWORD: "password",
        MAIL_PORT: "587"
    }):
        yield


def test_mail_config(mock_env_vars):
    config = mail_config()
    assert config[MAIL_HOST] == "smtp.mailtrap.io"
    assert config[MAIL_USER] == "user@example.com"
    assert config[MAIL_PASSWORD] == "password"
    assert config[MAIL_PORT] == "587"


def test_extract_page_numbers():
    response = "Page 238, Page 293, Page 894 are relevant!"
    result = extract_page_number(response)
    assert result == [894, 293, 238]


def test_remove_repeated_first_line():
    input_str = "First line\nFirst line\nSecond line\n"
    result = remove_repeated_first_line(input_str)
    assert result == "First line\nSecond line"


def test_remove_repeated_first_line_empty():
    input_str = ""
    result = remove_repeated_first_line(input_str)
    assert result == ""


@pytest.fixture
def mock_docs():
    doc1 = MagicMock()
    doc1.page_content = "First line\nFirst line\nSecond line\n"
    doc1.metadata = {}

    doc2 = MagicMock()
    doc2.page_content = "First line\nSecond line\n"
    doc2.metadata = {}

    return [(doc1, 0.9), (doc2, 0.8)]


def test_delete_repeating_lines_from_docs(mock_docs):
    result = delete_repeating_lines_from_docs(mock_docs)
    assert result[0][0].page_content == "First line\nSecond line"
    assert result[1][0].page_content == "First line\nSecond line"


def test_bin_images_to_text():
    images = [
        {"filename": "image1.jpg", "image_base64": "base64string1"},
        {"filename": "image2.jpg", "image_base64": "base64string2"}
    ]
    result = bin_images_to_text(images)
    assert result == "![image1.jpg](base64string1)\n![image2.jpg](base64string2)\n"


def test_get_erp_image_paths():
    with patch("glob.glob", return_value=["/path/to/image1", "/path/to/image2"]):
        result = get_erp_image_paths()
        assert result == ["/path/to/image1", "/path/to/image2"]


def test_get_erp_text_paths():
    with patch("glob.glob", return_value=["/path/to/text1", "/path/to/text2"]):
        result = get_erp_text_paths()
        assert result == ["/path/to/text1", "/path/to/text2"]
