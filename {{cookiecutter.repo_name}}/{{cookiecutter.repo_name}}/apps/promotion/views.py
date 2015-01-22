import logging

from django.views import generic


class HomeView(generic.TemplateView):
    template_name = "promotion/home.html"
