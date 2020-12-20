import orjson
import shortuuid

from django_unicorn.utils import generate_checksum


def test_message_call_method(client):
    data = {}
    message = {
        "actionQueue": [{"payload": {"name": "test_method"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("method_count") == 1


def test_message_call_method_redirect(client):
    data = {}
    message = {
        "actionQueue": [{"payload": {"name": "test_redirect"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert "redirect" in body
    redirect = body["redirect"]
    assert redirect.get("url") == "/something-here"
    assert redirect.get("refresh", False) == False


def test_message_call_method_refresh_redirect(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "test_refresh_redirect"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert "redirect" in body
    redirect = body["redirect"]
    assert redirect.get("url") == "/something-here"
    assert redirect.get("refresh")
    assert redirect.get("title") == "new title"


def test_message_call_method_hash_update(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "test_hash_update"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert "redirect" in body
    assert body["redirect"].get("hash") == "#test=1"


def test_message_call_method_return_value(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "test_return_value"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert "return" in body
    return_data = body["return"]
    assert return_data.get("method") == "test_return_value"
    assert return_data.get("params") == []
    assert return_data.get("value") == "booya"


def test_message_call_method_setter(client):
    data = {}
    message = {
        "actionQueue": [{"payload": {"name": "method_count=2"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("method_count") == 2


def test_message_call_method_nested_setter(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "nested.check=False"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("nested").get("check") == False


def test_message_call_method_toggle(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "$toggle('check')"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("check") == True


def test_message_call_method_nested_toggle(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "$toggle('nested.check')"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("nested").get("check") == True


def test_message_call_method_params(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "test_method_params(3)"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["data"].get("method_count") == 3


def test_message_call_method_no_validation(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "set_text_no_validation"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeValidationComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert not body["errors"]


def test_message_call_method_validation(client):
    data = {}
    message = {
        "actionQueue": [
            {"payload": {"name": "set_text_with_validation"}, "type": "callMethod",}
        ],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": shortuuid.uuid()[:8],
    }

    response = client.post(
        "/message/tests.views.fake_components.FakeValidationComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)

    assert body["errors"]
    assert body["errors"]["number"]
    assert body["errors"]["number"][0]["code"] == "required"
    assert body["errors"]["number"][0]["message"] == "This field is required."
