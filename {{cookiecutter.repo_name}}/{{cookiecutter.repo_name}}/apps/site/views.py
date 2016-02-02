import os.path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = 'text/plain'


def serve_apple_app_site_association(request):
    """
    More information on this file
    see: https://developer.apple.com/library/prerelease/ios/documentation/General/\
Conceptual/AppSearch/UniversalLinks.html#//apple_ref/doc/uid/TP40016308-CH12-SW2
    """
    # signed file
    # path = os.path.join(settings.BASE_DIR, "apple-app-site-association_signed")
    # content_type = 'application/pkcs7-mime'

    # unsigned file
    path = os.path.join(settings.BASE_DIR, "apple-app-site-association")
    # content_type = 'application/json'
    content_type = 'application/pkcs7-mime'

    try:
        with open(path, 'rb') as file:
            return HttpResponse(file, content_type=content_type)
    except EnvironmentError:
        raise Http404("The Apple App Site Association file is not readable")
