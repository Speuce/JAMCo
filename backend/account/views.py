"""
Account views

API-layer for account related operations.
"""
import logging
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
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

    body = read_request(request)
    credential = body['credential']
    logger.debug(f"get_or_create_account: {credential}")

    user = business.get_or_create_user({'google_id': credential})

    return JsonResponse({'data': user.id})


@require_POST
def update_account(request: HttpRequest):
    """
    Updates information about an account, given a google id token.
    """

    body = read_request(request)
    credential = body['google_id']
    logger.debug(f"update_account: {credential}")

    try:
        business.update_user(body)
    except (AttributeError, ObjectDoesNotExist, KeyError):
        # Complain if the frontend tried to modify fields that aren't part of
        # the User model (AttributeError), tries to modify a user that doesn't
        # exist (ObjectDoesNotExist), or doesn't supply the Google ID (KeyError)
        return JsonResponse(status=400, data={})

    return JsonResponse(status=200, data={})


@require_POST
def get_columns(request: HttpRequest):
    """
    Gets all of the columns for a given user
    """

    body = read_request(request)
    user_id = body['user_id']
    logger.debug(f'get_columns: {user_id}')

    try:
        columns = business.get_columns(user_id)

        return JsonResponse(
            status=200,
            data={'columns': [column.to_dict() for column in columns]}
        )
    except ObjectDoesNotExist:
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
    user_id = body['user_id']
    payload = body['payload']
    logger.debug(f'update_columns: {user_id}, {payload}')

    try:
        columns = business.update_columns(user_id, payload)
        return JsonResponse(
            status=200,
            data={'columns': [column.to_dict() for column in columns]}
        )
    except (ObjectDoesNotExist):
        return JsonResponse(status=400, data={})

