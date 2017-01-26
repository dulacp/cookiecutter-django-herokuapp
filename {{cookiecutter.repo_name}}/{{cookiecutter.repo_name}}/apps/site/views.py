import os.path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = 'text/plain'
