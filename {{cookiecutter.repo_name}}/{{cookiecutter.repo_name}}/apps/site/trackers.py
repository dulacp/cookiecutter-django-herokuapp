import logging
import uuid

from django.conf import settings

import requests
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def generate_default_client_id():
    """Google advise to generate a UUID4 value"""
    return uuid.uuid4()


def get_client_from_request(http_request):
    """
    The cookie format is the following : "GA<version>.<depth>.<user_id_part1>.<user_id_part2>"
    """
    if http_request is None:
        return generate_default_client_id()

    cookie_name = '_ga'
    cookie_value = http_request.COOKIES.get(cookie_name, None)
    if cookie_value is None:
        logger.info("User has no google analytics cookie named `{}`".format(cookie_name))
        return generate_default_client_id()

    if not cookie_value.startswith('G'):
        logger.warning("The user google analytics cookie doesn't respect the expected "
                       "format `G*`: '{}'".format(cookie_value))
        return generate_default_client_id()

    # parse the client id
    parts = cookie_value.split('.')

    if len(parts) != 4:
        logger.warning("The user google analytics cookie doesn't respect the expected "
                       "format: '{}'".format(cookie_value))
        return generate_default_client_id()

    client_id = ".".join(parts[-2:])  # restore the last two digits
    return client_id


def track_event(http_request, event_category, event_action, event_label):
    """
    Track the event based on the Measurement Protocol, part of the Universal Analytics
    https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide
    """
    tracking_id = settings.GOOGLE_ANALYTICS_ID
    if tracking_id is None:
        return False

    client_id = get_client_from_request(http_request)

    endpoint_url = "https://www.google-analytics.com/collect"
    params = {
        'v': 1,  # version
        'tid': tracking_id,
        'cid': client_id,

        't': 'event',
        'ec': event_category,  # category
        'ea': event_action,  # action
        'el': event_label,  # label
    }

    response = requests.post(endpoint_url, params)
    try:
        response.raise_for_status()
    except HTTPError as inst:
        logger.error(inst)
        return False
    return True
