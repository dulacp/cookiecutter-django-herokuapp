from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^', include('apps.promotion.urls', namespace="promotion")),

    url(r'^admin/', include(admin.site.urls)),
)


if settings.LOCAL_SERVER:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        # url(r'^404$', TemplateView.as_view(template_name='404.html')),
        # url(r'^500$', TemplateView.as_view(template_name='500.html')),
    )
