from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('apps.promotion.urls', namespace="promotion")),

    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


if settings.LOCAL_SERVER:
    from django.views.static import serve
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT}),
        # url(r'^404$', TemplateView.as_view(template_name='404.html')),
        # url(r'^500$', TemplateView.as_view(template_name='500.html')),
    ]
