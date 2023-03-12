from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

@ensure_csrf_cookie
def index(request):
    if settings.PROD:
        return render(request, "index.html")
    else:
       return render(request, "index-dev.html")     
