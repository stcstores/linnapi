import pytest

from linnapi.inventory import UpdateImageRequster
from linnapi.requests.inventory import UpdateImages


@pytest.fixture
def image_id():
    return "eea21827-491d-4022-996a-d068dd6b25ea"


@pytest.fixture
def stock_item_id():
    return "972af264-d768-4c6c-9152-0ad9d9d5b352"


@pytest.fixture
def sort_order():
    return 6


def test_update_image_requester_request_method():
    assert UpdateImageRequster().request_method == UpdateImages


def test_add_request_method(image_id, stock_item_id, sort_order):
    requester = UpdateImageRequster()
    requester.add_request(
        image_id=image_id,
        stock_item_id=stock_item_id,
        sort_order=sort_order,
        is_main=True,
    )
    assert requester.requests == [
        {
            "row_id": image_id,
            "stock_item_id": stock_item_id,
            "sort_order": sort_order,
            "is_main": True,
        }
    ]
