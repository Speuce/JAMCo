import json
from django.http import HttpRequest


def read_request(request: HttpRequest):
    """
    Reads the request body and returns it json decoded.
    """
    return json.loads(request.body.decode("utf-8"))
