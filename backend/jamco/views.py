from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import os

@ensure_csrf_cookie
def index(request):
    if os.getenv("PROD"):
#         return render(request, "index.html")
       raise ValueError("prod is true")
    else:
       return render(request, "index-dev.html")     
