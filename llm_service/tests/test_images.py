from unittest import mock
import base64
from unittest import mock

from services.images import bin_img_to_base64_dict, get_erp_images, \
    image_from_path


@mock.patch('os.path.basename')
@mock.patch('builtins.open', mock.mock_open(read_data=b"mock image data"))
def test_bin_img_to_base64_dict(mock_basename, mock_open):
    mock_basename.return_value = "image1.png"

    result = bin_img_to_base64_dict('mock_image_path.png')

    mock_open.assert_called_once_with('mock_image_path.png', 'rb')

    expected_base64 = base64.b64encode(b"mock image data").decode("utf-8")
    assert result == {
        "filename": "image1.png",
        "image_base64": f"data:image/png;base64,{expected_base64}"
    }


@mock.patch('glob.glob')
@mock.patch('utils.paper_utils.extract_page_number_from_path')
@mock.patch('services.images.bin_img_to_base64_dict')
def test_get_erp_images(mock_bin_img_to_base64_dict, mock_extract_page_number, mock_glob):
    mock_glob.return_value = ['path/to/p1.png', 'path/to/p2.png']
    mock_extract_page_number.side_effect = lambda x: int(x.split('p')[1].split('.')[0])
    mock_bin_img_to_base64_dict.return_value = {
        "filename": "p1.png",
        "image_base64": "mock_base64_1"
    }

    result = get_erp_images([1])

    mock_glob.assert_called_once_with('PAPERS_OUTPUT_IMAGES/p*')

    mock_extract_page_number.assert_called_with('path/to/p1.png')
    mock_bin_img_to_base64_dict.assert_called_with('path/to/p1.png')

    assert result == [{"filename": "p1.png", "image_base64": "mock_base64_1"}]


@mock.patch('services.images.bin_img_to_base64_dict')
def test_image_from_path(mock_bin_img_to_base64_dict):
    mock_bin_img_to_base64_dict.return_value = {
        "filename": "image1.png",
        "image_base64": "mock_base64_data"
    }

    result = image_from_path(['path/to/image1.png', 'path/to/image2.png'])

    mock_bin_img_to_base64_dict.assert_any_call('path/to/image1.png')
    mock_bin_img_to_base64_dict.assert_any_call('path/to/image2.png')

    assert result == [{'filename': 'image1.png', 'image_base64': 'mock_base64_data'},
                      {'filename': 'image1.png', 'image_base64': 'mock_base64_data'}]
