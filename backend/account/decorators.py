from django.http import JsonResponse
import logging

from account.business import validate_token

logger = logging.getLogger(__name__)


def requires_login(wrapped_view):
    def _decorator(request, *args, **kwargs):
        if request.COOKIES.get("auth_token"):
            token = request.COOKIES.get("auth_token")
            try:
                user = validate_token(token)
                request.user = user
                return wrapped_view(request, *args, **kwargs)
            except Exception as err_msg:
                return JsonResponse(status=401, data={"error": repr(err_msg)})
        else:
            return JsonResponse({}, status=401)

    return _decorator
