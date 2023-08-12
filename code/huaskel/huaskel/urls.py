"""huaskel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
import card_api.models
from card_api import models

admin.site.site_header = "HUA Admin"
admin.site.site_title = "HUA Admin Portal"
admin.site.index_title = "Welcome to HUA admin"
urlpatterns = [
    path('api/',include('card_api.urls')),
    path('i18n/', include('django.conf.urls.i18n'))] + \
    i18n_patterns(
    path('admin/', admin.site.urls, {'extra_context': {'mycontext': models.Station.objects.all().values()}}),
    #for future refrence to make it better (?)  https://stackoverflow.com/questions/39476439/add-context-to-every-django-admin-page
    path('', include('accounts.urls')),
)
