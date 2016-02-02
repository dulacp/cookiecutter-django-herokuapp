"""
NB: Be sure to import this module ONLY in the `app_confis.AppConfig.ready` method,
    otherwise there will be unwanted side-effects due to imports creating multiple
    signal connections.
"""

from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import invalidate_current_site_cache


@receiver(post_save, sender=Site)
def handle_new_user_creation(sender, instance, created, **kwargs):
    # we reset the site instance cache
    invalidate_current_site_cache()
