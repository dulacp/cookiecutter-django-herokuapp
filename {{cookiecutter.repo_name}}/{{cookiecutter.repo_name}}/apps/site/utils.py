import os.path

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import caches

CURRENT_SITE_INSTANCE_CACHE_KEY = 'current-site-object'


def get_current_site_from_cache():
    cache = caches['inmemory']
    return cache.get(CURRENT_SITE_INSTANCE_CACHE_KEY)


def update_current_site_cache(new_site):
    cache = caches['inmemory']
    cache.set(CURRENT_SITE_INSTANCE_CACHE_KEY, new_site)


def invalidate_current_site_cache():
    cache = caches['inmemory']
    cache.delete(CURRENT_SITE_INSTANCE_CACHE_KEY)


def canonical_url(url, use_protocol=True, protocol=None):
    """
    Ensure that the url contains the `https://mysite.com` part,
    particularly for requests made on the local dev server
    """
    if protocol is None:
        protocol = "https://" if use_protocol else "//"
        if settings.LOCAL_SERVER and not settings.LOCAL_HTTPS:
            protocol = "http://"

    if not url.startswith('http'):
        current_site = get_current_site_from_cache()
        if current_site is None:
            current_site = Site.objects.get(id=settings.SITE_ID)
            update_current_site_cache(current_site)
        url = "{}{}".format(
            protocol,
            os.path.join(current_site.domain, url.lstrip('/')))
    else:
        url = url.replace('http://', '%s' % protocol)
        url = url.replace('https://', '%s' % protocol)

    return url
