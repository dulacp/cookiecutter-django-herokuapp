from django.db import models


class TrackingCreateMixin(models.Model):
    date_created = models.DateTimeField("Date création",
                                        auto_now_add=True)

    class Meta:
        abstract = True


class TrackingUpdateMixin(models.Model):
    # This field is used by Haystack to reindex search
    date_updated = models.DateTimeField("Date mise à jour",
                                        auto_now=True,
                                        db_index=True)

    class Meta:
        abstract = True


class TrackingCreateAndUpdateMixin(TrackingCreateMixin,
                                   TrackingUpdateMixin,
                                   models.Model):
    class Meta:
        abstract = True


class RedirectToAfterPostMixin(object):
    """
    A redirect mixin to make it simpler to redirect to another page specified
    in the GET parameter `url`.

    For this to work you only need to include an hidden input in the form
    value the name `_return_url`
    """

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return_to_url = self.request.GET.get('url')
        ctx['return_url'] = return_to_url
        return ctx

    def get_success_url(self):
        return_to_url = self.request.POST.get('_return_url')
        if return_to_url is None:
            return super().get_success_url()
        return return_to_url
