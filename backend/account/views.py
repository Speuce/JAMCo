"""
Account views

API-layer for account related operations.
"""
import logging
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from google.oauth2 import id_token
from google.auth.transport import requests
from jamco.helper import read_request
from . import business

logger = logging.getLogger(__name__)

logger.debug("SETUP")


@require_POST
def get_or_create_account(request: HttpRequest):
    """
    Creates a new account, given google id token.
    Will use the google id token to get the user's information.
    """
    logger.debug("Here!")
    if not request.COOKIES.get("csrftoken"):
        return HttpResponse("No CSRF Token in Cookie", status=401)
    elif not request.headers.get("X-Csrftoken"):
        return HttpResponse("No CSRF Token in Header", status=401)
    elif request.COOKIES.get("csrftoken") != request.headers.get("X-Csrftoken"):
        return HttpResponse("CSRF Validation Failed", status=401)

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
        if idinfo["sub"]:
            logger.debug(f"Credential Validated for User.google_id: { idinfo['sub'] }")

            user = business.get_or_create_user(idinfo)
            logger.debug(f"Returned user:\n{user.to_dict()}")
            # Need some way to differenciate first-time logins
            # check user.last_login in frontend
            # if None -> first login, redirect to account setup
            # regardless, post to login_user endpoint to set value?
            return JsonResponse({"data": user.to_dict()})
        else:  # probably removable
            return HttpResponse("Token Authentication Failed", status=401)

    except ValueError as err_msg:
        # Invalid token
        logger.debug("Invalid Token")
        logger.debug(f"Error info:\n{err_msg}")
        return HttpResponse("Token Authentication Failed", status=401)


@require_POST
def update_account(request: HttpRequest):
    """
    Updates information about an account, given a google id token.
    """

    body = read_request(request)
    credential = body["google_id"]
    logger.debug(f"update_account: {credential}")

    try:
        business.update_user(body)
    except (AttributeError, ObjectDoesNotExist, KeyError) as err_msg:
        # Complain if the frontend tried to modify fields that aren't part of
        # the User model (AttributeError), tries to modify a user that doesn't
        # exist (ObjectDoesNotExist), or doesn't supply the Google ID (KeyError)
        logger.debug(f"Update error:\n{err_msg}")
        return JsonResponse(status=400, data={})

    return JsonResponse(status=200, data={})
