from django.conf import settings


def debug(context):
    return {"PROD": not settings.DEBUG}
