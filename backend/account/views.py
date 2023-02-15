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


@require_POST
def get_or_create_account(request: HttpRequest):
    """
    Creates a new account, given google id token.
    Will use the google id token to get the user's information.
    """
    if not request.COOKIES.get("csrftoken"):
        return HttpResponse("No CSRF Token in Cookie", status=401)
    elif not request.headers.get("X-Csrftoken"):
        return HttpResponse("No CSRF Token in Header", status=401)
    elif request.COOKIES.get("csrftoken") != request.headers.get(
            "X-Csrftoken"):
        return HttpResponse("CSRF Validation Failed", status=401)

    body = read_request(request)
    client_id = body["client_id"]
    credential = body["credential"]
    logger.debug(f"get_or_create_account: {credential}")
    logger.debug(f"body: {body}")

    # Verify Credentials via Google
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(credential,
                                              requests.Request(),
                                              client_id,
                                              clock_skew_in_seconds=5)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        logger.debug(
            f"Credential Validated for User.google_id: { idinfo['sub'] }")

        user, created = business.get_or_create_user(idinfo)
        return JsonResponse({"data": user.to_dict(), "created": created})

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


@require_POST
def get_columns(request: HttpRequest):
    """
    Gets all of the columns for a given user
    """

    body = read_request(request)
    user_id = body["user_id"]
    logger.debug(f"get_columns: {user_id}")

    try:
        columns = business.get_columns(user_id)

        return JsonResponse(
            status=200,
            data={'columns': [column.to_dict() for column in columns]})
    except Exception:
        return JsonResponse(status=400, data={})


@require_POST
def update_columns(request: HttpRequest):
    """
    Called when the user presses the save button on the frontend column view.
    Takes the user's list of columns (which have been updated on the frontend)
    and reflects those changes in the database. Returns all of the user's
    columns.
    """

    body = read_request(request)
    user_id = body["user_id"]
    payload = body["payload"]
    logger.debug(f"update_columns: {user_id}, {payload}")

    try:
        columns = business.update_columns(user_id, payload)
        return JsonResponse(
            status=200,
            data={'columns': [column.to_dict() for column in columns]})
    except Exception:
        return JsonResponse(status=400, data={})
