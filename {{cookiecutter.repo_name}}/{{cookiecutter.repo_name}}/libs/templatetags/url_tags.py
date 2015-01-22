# encoding: utf-8

from django import template
from django.http import QueryDict

from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument, MultiValueArgument

from libs.utils import canonical_url

register = template.Library()


@register.filter('canonical')
def _get_canonical_url(url):
    return canonical_url(url, protocol="http:")


class QueryParameters(Tag):
    name = 'query'
    options = Options(
        MultiKeywordArgument('kwa'),
    )

    def render_tag(self, context, kwa):
        q = QueryDict('').copy()
        q.update(kwa)
        return q.urlencode()

register.tag(QueryParameters)


class GetParameters(Tag):

    """
    {% raw %}{% get_parameters [except_field, ] %}{% endraw %}
    """
    name = 'get_parameters'
    options = Options(
        MultiValueArgument('except_fields', required=False),
    )

    def render_tag(self, context, except_fields):
        try:
            # If there's an exception (500), default context_processors may not
            # be called.
            request = context['request']
        except KeyError:
            return context

        getvars = request.GET.copy()

        for field in except_fields:
            if field in getvars:
                del getvars[field]

        return getvars.urlencode()

register.tag(GetParameters)
