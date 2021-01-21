import time
from copy import deepcopy
from multiprocessing.dummy import Pool as ThreadPool

import orjson
import pytest
import shortuuid

from django_unicorn.components import UnicornView
from django_unicorn.utils import generate_checksum


class FakeSlowComponent(UnicornView):
    template_name = "templates/test_component.html"

    counter = 0
    another_thing = 0

    def slow_action(self):
        time.sleep(0.3)
        self.counter += 1

        return self.counter


@pytest.mark.slow
def test_message_call_method_single(client):
    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
        "epoch": time.time(),  # assert there is an epoch (or set it in Python?)
    }

    response = client.post(
        "/message/tests.views.message.test_call_method_multiple.FakeSlowComponent",
        message,
        content_type="application/json",
    )

    body = orjson.loads(response.content)
    assert body["data"].get("counter") == 1


def _message_runner(args):
    client = args[0]
    sleep_time = args[1]
    message = args[2]
    time.sleep(sleep_time)

    # TODO: assert there is an epoch (or set it in Python?) in component request init
    message["epoch"] = time.time()

    response = client.post(
        "/message/tests.views.message.test_call_method_multiple.FakeSlowComponent",
        message,
        content_type="application/json",
    )
    return response


@pytest.mark.slow
def test_message_call_method_two(client):
    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.1, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        # print("first_body", first_body)
        assert first_body["data"].get("counter") == 2

        second_result = results[1]
        second_body = orjson.loads(second_result.content)
        assert second_body["queued"] == True


@pytest.mark.slow
def test_message_call_method_multiple(client):
    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.1, message), (client, 0.2, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == len(results)

        for result in results[1:]:
            result = results[1]
            body = orjson.loads(result.content)
            assert body.get("queued") == True


@pytest.mark.slow
<<<<<<< HEAD
def test_message_call_method_multiple_with_updated_data(client):
=======
def test_message_multiple_return_is_correct(client, settings):
    _set_serial(settings, True, 5)

    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.1, message), (client, 0.2, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == len(results)
        assert first_body["return"].get("value") == len(results)

        for result in results[1:]:
            result = results[1]
            body = orjson.loads(result.content)
            assert body.get("queued") == True


@pytest.mark.slow
def test_message_multiple_with_updated_data(client, settings):
    """
    Not sure how likely this is to happen, but if the data got changed in a new queued request
    it gets disregarded because no sane way to merge it together. Not ideal, but not sure how to
    handle it.
    """
    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.1, message), (client, 0.2, message)]

    # This new message with different data won't get used because not
    # sure how to reconcile this with resulting data from queued messages
    message_with_new_data = deepcopy(message)
    message_with_new_data["data"] = {"counter": 7}
    message_with_new_data["checksum"] = generate_checksum(
        orjson.dumps(message_with_new_data["data"])
    )
    messages.append((client, 0.4, message_with_new_data))

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == 4

        for result in results[1:]:
            result = results[1]
            body = orjson.loads(result.content)
            assert body.get("queued") == True


@pytest.mark.slow
def test_message_second_request_not_queued_because_after_first(client, settings):
    _set_serial(settings, True, 5)

    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.4, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == 1

        second_result = results[1]
        second_body = orjson.loads(second_result.content)
        assert second_body["data"].get("counter") == 1


@pytest.mark.slow
def test_message_second_request_not_queued_because_serial_timeout(client, settings):
    _set_serial(settings, True, 0.1)

    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.2, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == 1

        second_result = results[1]
        second_body = orjson.loads(second_result.content)
        assert second_body["data"].get("counter") == 1


@pytest.mark.slow
def test_message_second_request_not_queued_because_serial_disabled(client, settings):
    _set_serial(settings, False, 5)

    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.2, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == 1

        second_result = results[1]
        second_body = orjson.loads(second_result.content)
        assert second_body["data"].get("counter") == 1


@pytest.mark.slow
def test_message_second_request_not_queued_because_dummy_cache(client, settings):
    _set_serial(
        settings, True, 5, cache_backend="django.core.cache.backends.dummy.DummyCache"
    )

    data = {"counter": 0}
    component_id = shortuuid.uuid()[:8]
    message = {
        "actionQueue": [{"payload": {"name": "slow_action"}, "type": "callMethod",}],
        "data": data,
        "checksum": generate_checksum(orjson.dumps(data)),
        "id": component_id,
    }
    messages = [(client, 0, message), (client, 0.2, message)]

    with ThreadPool(len(messages)) as pool:
        results = pool.map(_message_runner, messages)
        assert len(results) == len(messages)

        first_result = results[0]
        first_body = orjson.loads(first_result.content)
        assert first_body["data"].get("counter") == 1

        second_result = results[1]
        second_body = orjson.loads(second_result.content)
        assert second_body["data"].get("counter") == 1
