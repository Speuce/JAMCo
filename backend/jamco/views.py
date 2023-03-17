from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from account.models import User

from jamco import settings

from logging import getLogger

logger = getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    logger.info("Access to index.html")
    if settings.IS_TEST:
        User.objects.filter(google_id="1234567890").delete()
        User.objects.filter(google_id="0987654321").delete()
    return render(request, "index.html")
