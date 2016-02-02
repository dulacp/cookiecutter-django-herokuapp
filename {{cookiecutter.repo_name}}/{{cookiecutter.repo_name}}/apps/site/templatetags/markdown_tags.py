import markdown
from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import Tag
from django import template
from django.template.context import RequestContext
from django.template.loader import get_template

register = template.Library()


class Markdown(Tag):
    name = 'markdown'
    options = Options(
        Argument('name', resolve=False),
    )

    def render_tag(self, context, name):
        template_name = context.get(name, name)
        parser = markdown.Markdown()
        tmpl = get_template(template_name)
        tmpl_context = context
        if isinstance(tmpl_context, RequestContext):
            tmpl_context = tmpl_context.flatten()
        content = tmpl.render(tmpl_context)
        return parser.convert(content)


register.tag(Markdown)
