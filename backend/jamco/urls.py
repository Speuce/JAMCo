"""jamco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from account import views as account_views
from column import views as column_views
from job import views as job_views
from .views import index

urlpatterns = [
    path("", index),
    path("sandbox", index),
    path("admin/", admin.site.urls),
    path(
        "account/api/get_or_create_account",
        account_views.get_or_create_account,
        name="get_or_create_account",
    ),
    path(
        "account/api/update_account",
        account_views.update_account,
        name="update_account",
    ),
    path("account/api/update_privacies", account_views.update_privacies, name="update_privacies"),
    path("account/api/get_user_privacies", account_views.get_user_privacies, name="get_user_privacies"),
    path("account/api/search_users_by_name", account_views.search_users_by_name, name="search_users_by_name"),
    path("account/api/add_friend", account_views.add_friend, name="add_friend"),
    path("account/api/remove_friend", account_views.remove_friend, name="remove_friend"),
    path("account/api/validate_auth_token", account_views.validate_auth_token, name="validate_auth_token"),
    path("account/api/create_friend_request", account_views.create_friend_request, name="create_friend_request"),
    path("account/api/accept_friend_request", account_views.accept_friend_request, name="accept_friend_request"),
    path("account/api/deny_friend_request", account_views.deny_friend_request, name="deny_friend_request"),
    path(
        "account/api/get_friend_requests_status",
        account_views.get_friend_requests_status,
        name="get_friend_requests_status",
    ),
    path("column/api/get_columns", column_views.get_columns, name="get_columns"),
    path(
        "column/api/update_columns",
        column_views.update_columns,
        name="update_columns",
    ),
    path("job/api/get_minimum_jobs", job_views.get_minimum_jobs, name="get_minimum_jobs"),
    path("job/api/get_job_by_id", job_views.get_job_by_id, name="get_job_by_id"),
    path("job/api/create_job", job_views.create_job, name="create_job"),
    path("job/api/update_job", job_views.update_job, name="update_job"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
