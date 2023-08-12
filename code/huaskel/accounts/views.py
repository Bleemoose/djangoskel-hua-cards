from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import extMailForm, forgotPasswordForm, changePasswordForm, verifyPasswordForm
from .tokenhandler import send_activation_token, create_activation_token, send_reset_token, create_reset_token
from .models import Token
from .ldaphandler import ldapConnection
from django.urls import reverse
import logging
from django.contrib.auth.models import Permission

# Create your views here.

logger = logging.getLogger('huaskel')

def index(request):
    """
    Index view
    """
    return render(request, 'accounts/index.html')

@login_required
def profile(request):
    """
    Profive View
    """
    user = request.user
    username = user.username
    #for debug reasons
    perm_tuple = [(x.id, x.name) for x in Permission.objects.filter(user=user)]
    print(perm_tuple)
    logger.info('User %s has accessed his profile page' %username)

    return render(request,'accounts/profile.html', context = {'user' : user})

@login_required
def logoutView(request):
    logger.info('User %s has logged out' %request.user.username)
    logout(request)
    return render(request,'accounts/byebye.html')

def forgotpassword(request):
    return HttpResponse('Forgot password view')
