from django.http import JsonResponse

import account.business as business
import jamco.helper as helper


def requires_login(allow_friends=False, check_field="user_id"):
    def _inner(wrapped_view):
        def _decorator(request, *args, **kwargs):
            if request.COOKIES.get("auth_token"):
                token = request.COOKIES.get("auth_token")
                try:
                    user = business.validate_token(token)
                    request.user = user
                    body = helper.read_request(request)
                    if check_field is not None and body.get(check_field) != user.id:
                        if not allow_friends:
                            return JsonResponse({}, status=401)
                        else:
                            if not user.friends.filter(id=body.get(check_field)).exists():
                                return JsonResponse({}, status=401)
                    return wrapped_view(request, *args, **kwargs)
                except Exception as e:
                    return JsonResponse(status=401, data={})
            else:
                return JsonResponse({}, status=401)

        return _decorator

    return _inner
