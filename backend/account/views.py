"""
Account views

API-layer for account related operations.
"""
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from jamco.helper import read_request

import logging

logger = logging.getLogger(__name__)

logger.debug("SETUP")


@require_POST
def get_or_create_account(request: HttpRequest):
    """
    Creates a new account, given google id token.
    Will use the google id token to get the user's information.
    """

    body = read_request(request)
    credential = body['credential']
    logger.debug(f"get_or_create_account: {credential}")

    #TODO: Create account, return created account
    return JsonResponse({'data': "account_created"})