"""
test
"""
from django.shortcuts import render


def index(request):
    """
    test
    """
    return render(request, "index.html")
