import types

import orjson
import pytest

from django_unicorn.components import UnicornView


class ExampleComponent(UnicornView):
    name = "World"

    def get_name(self):
        return "World"


@pytest.fixture(scope="module")
def component():
    return ExampleComponent(component_id="asdf1234", component_name="example")


def test_init_with_template_name():
    class TestComponent(UnicornView):
        template_name = "unicorn/test.html"

    component = TestComponent(component_id="asdf1234", component_name="hello-world")
    assert component.template_name == "unicorn/test.html"


def test_init_with_get_template_names():
    class TestComponent(UnicornView):
        def get_template_names(self):
            return []

    component = TestComponent(component_id="asdf1234", component_name="hello-world")
    assert component.template_name is None


def test_init_attribute_names_cache(component):
    attribute_names_cache = component._attribute_names_cache
    assert len(attribute_names_cache) == 1
    assert attribute_names_cache[0] == "name"


def test_init_attribute_names(component):
    attribute_names = component._attribute_names()
    assert len(attribute_names) == 1
    assert attribute_names[0] == "name"


def test_init_attributes(component):
    attributes = component._attributes()
    assert len(attributes) == 1
    assert attributes["name"] == "World"


def test_init_properties():
    class TestComponent(UnicornView):
        @property
        def name(self):
            return "World"

    component = TestComponent(component_id="asdf1234", component_name="hello-world")
    attributes = component._attributes()
    assert len(attributes) == 1
    assert attributes["name"] == "World"


def test_init_methods_cache(component):
    assert len(component._methods_cache) == 1


def test_init_methods(component):
    methods = component._methods()
    assert len(methods) == 1
    assert methods["get_name"]() == "World"


def test_get_frontend_context_variables(component):
    frontend_context_variables = component.get_frontend_context_variables()
    frontend_context_variables_dict = orjson.loads(frontend_context_variables)
    assert len(frontend_context_variables_dict) == 1
    assert frontend_context_variables_dict.get("name") == "World"


def test_get_context_data(component):
    context_data = component.get_context_data()
    assert (
        len(context_data) == 4
    )  # `unicorn` and `view` are added to context data by default
    assert context_data.get("name") == "World"
    assert isinstance(context_data.get("get_name"), types.MethodType)


def test_is_public(component):
    assert component._is_public("test_name")


def test_is_public_protected(component):
    assert component._is_public("_test_name") == False


def test_is_public_http_method_names(component):
    assert component._is_public("http_method_names") == False
