from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.HomeView.as_view(),
        name="home"),
)
