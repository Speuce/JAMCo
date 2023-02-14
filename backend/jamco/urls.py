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
from account import views as account_views
from .views import index

urlpatterns = [
    path('', index),
    path('sandbox', index),
    path('admin/', admin.site.urls),
    path('account/api/get_or_create_account',
         account_views.get_or_create_account, name='get_or_create_account'),
    path('account/api/update_account',
         account_views.update_account, name='update_account'),
    path('account/api/get_columns',
        account_views.get_columns, name='get_columns'),
    path('account/api/update_columns',
        account_views.update_columns, name='update_columns'),
]
