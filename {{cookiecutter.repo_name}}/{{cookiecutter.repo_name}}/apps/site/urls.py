from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.views import generic

from . import views


urlpatterns = (
    url(r'^robots\.txt$', views.RobotsView.as_view(), name="robots"),
)


if getattr(settings, 'LOADERIO_TOKEN', None):
    loaderio_token = settings.LOADERIO_TOKEN

    class LoaderioTokenView(generic.View):
        def get(self, request, *args, **kwargs):
            return HttpResponse('{}'.format(loaderio_token))

    urlpatterns += (
        url(r'^{}/$'.format(loaderio_token), LoaderioTokenView.as_view()),
    )
