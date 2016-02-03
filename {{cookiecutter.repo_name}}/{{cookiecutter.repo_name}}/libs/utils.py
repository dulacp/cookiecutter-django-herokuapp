import copy
import datetime
import decimal
import hashlib
import os.path
import random
import uuid

from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str


def banker_round(decimal_value):
    """
    Force the value to be rounded with the `ROUND_HALF_EVEN` method,
    also called the Banking Rounding due to the heavy use in the
    banking system
    """
    return decimal_value.quantize(decimal.Decimal('0.01'),
                                  rounding=decimal.ROUND_HALF_EVEN)


def random_token(extra=None, hash_func=hashlib.sha256):
    """
    Extracted from `django-user-accounts`
    """
    if extra is None:
        extra = []
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits)).hexdigest()


def create_hash(string, hash_func=hashlib.sha256):
    """
    Create a 10-caracters string hash
    """
    _hash = hash_func(string)
    return _hash.hexdigest()[:10]


def nested_hash(data):
    """
    Make a hash from a nested dictionnary
    """

    if isinstance(data, (set, tuple, list)):
        return tuple(nested_hash(d) for d in data)

    elif not isinstance(data, dict):
        return data

    new_data = copy.deepcopy(data)
    for k, v in new_data.items():
        new_data[k] = nested_hash(v)

    return hash(tuple(frozenset(sorted(new_data.items()))))


@deconstructible
class UniqueFilename(object):

    def __init__(self, sub_path, original_filename_field=None):
        self.sub_path = sub_path
        self.original_filename_field = original_filename_field

    def __call__(self, instance, filename):
        if self.original_filename_field and hasattr(instance, self.original_filename_field):
            setattr(instance, self.original_filename_field, filename)
        parts = filename.split('.')
        extension = parts[-1]
        directory_path = os.path.normpath(datetime.datetime.now().strftime(force_str(self.sub_path)))
        unique_name = "{0}.{1}".format(uuid.uuid4(), extension)
        return os.path.join(directory_path, unique_name)


def queryset_iterator(queryset, chunksize=1000, reverse=False):
    """
    Execute the request by chunks to avoid database memory error
    """
    ordering = '-' if reverse else ''
    queryset = queryset.order_by(ordering + 'pk')
    last_pk = None
    new_items = True
    while new_items:
        new_items = False
        chunk = queryset
        if last_pk is not None:
            func = 'lt' if reverse else 'gt'
            chunk = chunk.filter(**{'pk__' + func: last_pk})
        chunk = chunk[:chunksize]
        row = None
        for row in chunk:
            yield row
        if row is not None:
            last_pk = row.pk
            new_items = True


def dict_match_items(a, b):
    shared_items = set(a.items()) & set(b.items())
    return shared_items


def dict_unmatch_items(a, b):
    unmatched_items = set(a.items()) ^ set(b.items())
    return unmatched_items
