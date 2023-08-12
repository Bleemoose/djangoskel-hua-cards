from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.getCards),
    path('checkInCard', views.checkInCard),
    path('getCardRegistriesForUser', views.getCardRegistriesForUser)
]