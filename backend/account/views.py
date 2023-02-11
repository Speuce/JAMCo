"""
Account views

API-layer for account related operations.
"""
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from jamco.helper import read_request
from . import business

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
def create_column(request: HttpRequest):
    """
    Creates a column for a user, given the user's google id and a column name
    """

    body = read_request(request)
    credential = body['google_id']
    column_name = body['column_name']
    logger.debug(f'create_column: {credential}, {column_name}')

    try:
        new_column = business.create_column(credential, column_name)
        return JsonResponse(status=200, data=new_column.to_dict())
    except ObjectDoesNotExist:
        return JsonResponse(status=400, data={})


@require_POST
def get_columns(request: HttpRequest):
    """
    Gets all of the columns for a given user
    """

    body = read_request(request)
    credential = body['google_id']
    logger.debug(f'create_column: {credential}')

    try:
        columns = business.get_columns(credential)

        return JsonResponse(
            status=200,
            data={'columns': [column.to_dict() for column in columns]}
        )
    except ObjectDoesNotExist:
        return JsonResponse(status=400, data={})


def rename_column(request: HttpRequest):
    """
    Renames the specified column
    """

    body = read_request(request)

    credential = body['google_id']
    column_number = body['column_number']
    new_name = body['new_name']

    logger.debug(
        f'rename_column: {credential} changed column {column_number} to \
            {new_name}'
    )

    try:
        column = business.rename_column(credential, column_number, new_name)
        return JsonResponse(status=200, data={'column': column.to_dict()})
    except ObjectDoesNotExist:
        return JsonResponse(status=400, data={})
