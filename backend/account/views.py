"""
Account views

API-layer for account related operations.
"""
import logging
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from google.oauth2 import id_token
from google.auth.transport import requests
from account.decorators import requires_login
from account.stubs import stub_verify_oauth2_token
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
        idinfo = None
        if not settings.IS_TEST:
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), client_id, clock_skew_in_seconds=5)
        else:
            idinfo = stub_verify_oauth2_token(credential, client_id)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        logger.debug(f"Credential Validated for User.google_id: { idinfo['sub'] }")

        user, token = business.get_or_create_user(idinfo)
        return JsonResponse({"data": user.to_dict(), "token": token})

    except ValueError as err_msg:
        # Invalid token
        logger.debug(f"Invalid Token: {err_msg}")
        return JsonResponse(status=401, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="id")
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


@require_POST
@requires_login()
def update_privacies(request: HttpRequest):
    """
    Updates privacy settings given a user id
    """

    body = read_request(request)
    logger.debug(f"update_privacies: {body}")

    try:
        business.update_privacies(body)
    except Exception as err_msg:
        logger.debug(f"Update error:\n{err_msg}")
        return JsonResponse(status=400, data={"error": repr(err_msg)})

    return JsonResponse(status=200, data={})


@require_POST
@requires_login(allow_friends=True)
def get_user_privacies(request: HttpRequest):
    """
    Gets Privacy options for the specified user
    """

    body = read_request(request)
    logger.debug(f"get_user_privacies: {body}")
    user_id = body.get("user_id")

    logger.debug(f"get_user_privacies: user: {user_id}")

    try:
        priv = business.get_privacies(user_id)
        return JsonResponse(data=priv.to_dict())
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="user1_id")
def remove_friend(request: HttpRequest):
    """
    Takes two users' ids and makes it so those two users are no longer friends with each other. If they weren't friends
    before, this method doesn't do anything.
    """

    try:
        body = read_request(request)
        user1_id = body["user1_id"]
        user2_id = body["user2_id"]
        logger.debug(f"add_friend: {user1_id}, {user2_id}")

        business.remove_friend(user1_id, user2_id)
        return JsonResponse(status=200, data={})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def validate_auth_token(request: HttpRequest):
    """
    Authenticates auth_token retrieved from local cookies
    """

    token = read_request(request)
    logger.debug(f"validate_auth_token: {token}")

    try:
        user, new_token = business.authenticate_token(token)
        return JsonResponse({"user": user.to_dict(), "token": new_token})
    except ObjectDoesNotExist as err_msg:
        logger.debug(f"Invalid Token: {err_msg}")
        return JsonResponse(status=401, data={"error": repr(err_msg)})


@require_POST
def get_updated_user_data(request: HttpRequest):
    """
    Authenticates auth_token retrieved from local cookies, without creating a new cookie
    """

    token = read_request(request)
    logger.debug(f"get_updated_user_data: {token}")

    try:
        user = business.validate_token(token)
        return JsonResponse({"user": user.to_dict()})
    except ObjectDoesNotExist as err_msg:
        logger.debug(f"Invalid Token: {err_msg}")
        return JsonResponse(status=401, data={"error": repr(err_msg)})


@require_POST
def search_users_by_name(request: HttpRequest):
    """
    Searches for [searchable] users by name
    """

    search_str = read_request(request)
    logger.debug(f"Searching for users like '{search_str}'")
    users_list = business.search_users_by_name(search_str)
    return JsonResponse(data={"user_list": users_list})


@require_POST
@requires_login(check_field="from_user_id")
def create_friend_request(request: HttpRequest):
    """
    Creates new FriendRequest
    """

    try:
        body = read_request(request)
        from_user_id = body["from_user_id"]
        to_user_id = body["to_user_id"]
        logger.debug(f"create_friend_request: {from_user_id} -> {to_user_id}")

        req = business.create_friend_request(from_user_id=from_user_id, to_user_id=to_user_id)
        return JsonResponse(data=req.to_dict())
    except (ObjectDoesNotExist, ValueError) as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="to_user_id")
def accept_friend_request(request: HttpRequest):
    """
    Accepts friend request sent to this user (the user sending accept)
    """

    try:
        body = read_request(request)
        request_id = body["request_id"]
        from_user_id = body["from_user_id"]
        to_user_id = body["to_user_id"]
        logger.debug(f"accept_friend_request: ToUser:{to_user_id}, FromUser:{from_user_id}, Request: {request_id}")

        business.accept_friend_request(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id)
        return JsonResponse(status=200, data={})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="to_user_id")
def deny_friend_request(request: HttpRequest):
    """
    Denies friend request sent to this user (the user sending deny)
    """

    try:
        body = read_request(request)
        request_id = body["request_id"]
        from_user_id = body["from_user_id"]
        to_user_id = body["to_user_id"]
        logger.debug(f"deny_friend_request: ToUser:{to_user_id}, FromUser:{from_user_id}, Request: {request_id}")

        business.deny_friend_request(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id)
        return JsonResponse(status=200, data={})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="user_id")
def get_friend_requests_status(request: HttpRequest):
    """
    Get sent & received requests for a user
    """

    try:
        body = read_request(request)
        user_id = body["user_id"]
        logger.debug(f"get_friend_requests_status: {user_id}")

        sent, received = business.get_friend_requests_status(user_id=user_id)

        return JsonResponse(data={"sent": list(sent), "received": list(received)})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
@requires_login(check_field="user_id")
def get_friend_data(request: HttpRequest):
    """
    Retrieve data of a friend of the user
    """

    try:
        body = read_request(request)
        user_id = body["user_id"]
        friend_id = body["friend_id"]
        logger.debug(f"get_friend_data: Getting info from user {friend_id} for user {user_id}")

        friend = business.get_friend_data(user_id=user_id, friend_id=friend_id)

        return JsonResponse({"friend": friend.to_dict()})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})
