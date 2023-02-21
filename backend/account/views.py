"""
Account views

API-layer for account related operations.
"""
import logging
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from google.oauth2 import id_token
from google.auth.transport import requests
from jamco.helper import read_request
from . import business

logger = logging.getLogger(__name__)


@require_POST
def get_or_create_account(request: HttpRequest):
    """
    Creates a new account, given google id token.
    Will use the google id token to get the user's information.
    """
    if not request.COOKIES.get("csrftoken"):
        return JsonResponse(status=401, data={"error": "No CSRF Token in Cookie"})
    elif not request.headers.get("X-Csrftoken"):
        return JsonResponse(status=401, data={"error": "No CSRF Token in Header"})
    elif request.COOKIES.get("csrftoken") != request.headers.get("X-Csrftoken"):
        return JsonResponse(status=401, data={"error": "CSRF Validation Failed"})

    body = read_request(request)
    client_id = body["client_id"]
    credential = body["credential"]
    logger.debug(f"get_or_create_account: {credential}")
    logger.debug(f"body: {body}")

    # Verify Credentials via Google
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            credential, requests.Request(), client_id, clock_skew_in_seconds=5
        )

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        logger.debug(f"Credential Validated for User.google_id: { idinfo['sub'] }")

        user, created = business.get_or_create_user(idinfo)
        return JsonResponse({"data": user.to_dict(), "created": created})

    except ValueError as err_msg:
        # Invalid token
        logger.debug(f"Invalid Token: {err_msg}")
        return JsonResponse(status=401, data={"error": repr(err_msg)})


@require_POST
def update_account(request: HttpRequest):
    """
    Updates information about an account, given a google id token.
    """

    body = read_request(request)
    logger.debug(f"update_account: {id}")

    try:
        business.update_user(body)
    except (AttributeError, ObjectDoesNotExist, KeyError) as err_msg:
        # Complain if the frontend tried to modify fields that aren't part of
        # the User model (AttributeError), tries to modify a user that doesn't
        # exist (ObjectDoesNotExist), or doesn't supply the Google ID (KeyError)
        logger.debug(f"Update error:\n{err_msg}")
        return JsonResponse(status=400, data={"error": repr(err_msg)})

    return JsonResponse(status=200, data={})
