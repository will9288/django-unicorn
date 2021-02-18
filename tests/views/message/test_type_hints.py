from decimal import Decimal

import orjson

from django_unicorn.components import UnicornView
from tests.views.message.utils import post_and_get_response


class FakeObjectsComponent(UnicornView):
    template_name = "templates/test_component.html"

    decimal_example: Decimal = Decimal(1.1)
    float_example: float = 1.2
    int_example: int = 3

    def assert_int(self):
        assert self.int_example == 4

    def assert_float(self):
        assert self.float_example == 1.3

    def assert_decimal(self):
        assert self.decimal_example == Decimal(1.5)


FAKE_OBJECTS_COMPONENT_URL = (
    "/message/tests.views.message.test_type_hints.FakeObjectsComponent"
)


def test_message_int(client):
    data = {"int_example": "4"}
    action_queue = [{"payload": {"name": "assert_int"}, "type": "callMethod",}]
    response = post_and_get_response(
        client, url=FAKE_OBJECTS_COMPONENT_URL, data=data, action_queue=action_queue,
    )

    body = orjson.loads(response.content)

    assert not body.get(
        "error"
    )  # UnicornViewError/AssertionError returns a a JsonResponse with "error" key
    assert not body["errors"]


def test_message_float(client):
    data = {"float_example": "1.3"}
    action_queue = [{"payload": {"name": "assert_float"}, "type": "callMethod",}]
    response = post_and_get_response(
        client, url=FAKE_OBJECTS_COMPONENT_URL, data=data, action_queue=action_queue,
    )

    body = orjson.loads(response.content)

    assert not body.get(
        "error"
    )  # UnicornViewError/AssertionError returns a a JsonResponse with "error" key
    assert not body["errors"]


def test_message_decimal(client):
    data = {"decimal_example": "1.5"}
    action_queue = [{"payload": {"name": "assert_decimal"}, "type": "callMethod",}]
    response = post_and_get_response(
        client, url=FAKE_OBJECTS_COMPONENT_URL, data=data, action_queue=action_queue,
    )

    body = orjson.loads(response.content)

    assert not body.get(
        "error"
    )  # UnicornViewError/AssertionError returns a a JsonResponse with "error" key
    assert not body["errors"]

