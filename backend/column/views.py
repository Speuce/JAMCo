"""
Account views

API-layer for account related operations.
"""
import logging
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from jamco.helper import read_request
from . import business

logger = logging.getLogger(__name__)


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
            status=200, data={"columns": [column.to_dict() for column in columns]}
        )
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


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
            status=200, data={"columns": [column.to_dict() for column in columns]}
        )
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})
