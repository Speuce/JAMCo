from django.conf import settings


def debug(context):
    return {"PROD": settings.PROD}
