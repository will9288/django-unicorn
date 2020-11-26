from django import template
from django.conf import settings

import shortuuid

from ..components import UnicornView
from ..settings import get_setting


register = template.Library()


@register.inclusion_tag("unicorn/scripts.html")
def unicorn_scripts():
    return {"MINIFIED": get_setting("MINIFIED", not settings.DEBUG)}


@register.inclusion_tag("unicorn/errors.html", takes_context=True)
def unicorn_errors(context):
    return {"unicorn": {"errors": context.get("unicorn", {}).get("errors", {})}}


def unicorn(parser, token):
    contents = token.split_contents()

    if len(contents) < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires at least a single argument" % token.contents.split()[0]
        )

    tag_name = contents[0]
    component_name = contents[1]

    if not (
        component_name[0] == component_name[-1] and component_name[0] in ('"', "'")
    ):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )

    args = contents[2:]

    return UnicornNode(component_name[1:-1], args)


class UnicornNode(template.Node):
    def __init__(self, component_name, args):
        self.component_name = component_name
        self.args = args

    def render(self, context):
        formatted_args = []

        for arg in self.args:
            try:
                formatted_args.append(template.Variable(arg).resolve(context))
            except TypeError:
                formatted_args.append(arg)
            except template.VariableDoesNotExist:
                formatted_args.append(arg)

        component_id = shortuuid.uuid()[:8]

        view = UnicornView.create(
            component_id=component_id,
            component_name=self.component_name,
            args=formatted_args,
        )
        rendered_component = view.render(init_js=True)

        return rendered_component


register.tag("unicorn", unicorn)
