import pytest

from linnapi.inventory import DeleteImagesRequester
from linnapi.requests.inventory import DeleteImagesFromInventoryItem


@pytest.fixture
def image_url():
    return "http://test.com/image_1.jpg"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def sort_order():
    return 6


def test_update_image_requester_request_method():
    assert DeleteImagesRequester().request_method == DeleteImagesFromInventoryItem


def test_add_request_method(image_url, stock_item_id, sort_order):
    requester = DeleteImagesRequester()
    requester.add_request(
        image_url=image_url,
        stock_item_id=stock_item_id,
    )
    assert requester.requests == [
        {
            "image_url": image_url,
            "stock_item_id": stock_item_id,
        }
    ]
