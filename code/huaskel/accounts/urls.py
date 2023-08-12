from django.urls import path, include

from . import views

urlpatterns = [
    # Index view
    path('', views.index, name = 'index'),
    path('accounts/profile/', views.profile, name = 'profile'),
    path('accounts/forgotpassword/', views.forgotpassword, name = 'forgotpassword'),
    path('accounts/logout/', views.logoutView, name = 'logout'),
    path('accounts/', include('django.contrib.auth.urls'))

]
