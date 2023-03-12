from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import os

@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")
