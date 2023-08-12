from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Token
import secrets
from django.utils import timezone
import datetime
from huaskel import settings
from django.urls import reverse

def delete_previous_tokens(username , type):
    """
    Delete previous tokens for the same account
    """
    tokens = Token.objects.filter(username = username,type = type)
    for token in tokens:
        token.delete()

def create_token(username, email, sze, duration, type):
    """
    Create account activation or forgot password tokens
    """
    delete_previous_tokens(email, type)
    random_token = secrets.token_hex(sze)
    expiration_time = timezone.now() + datetime.timedelta( days = duration )
    token = Token(token = random_token, username = username, expiration = expiration_time, externalMail = email,type=type)
    token.save()

    return token.pk

def create_activation_token(username, email):
    """
    Create activation token
    """
    delete_previous_tokens(username, 'activation')

    return create_token(username, email,settings.TOKEN_ACTIVATION_SIZE,
                        settings.TOKEN_ACTIVATION_DURATION,'activation')

def create_reset_token(username, email):
    """
    Create password reset token
    """
    delete_previous_tokens(username, 'reset')

    return create_token(username, email, settings.TOKEN_RESET_SIZE,
                        settings.TOKEN_RESET_DURATION,'reset')

def build_confirmation_url(token):
    """
    Build the activation token URL
    """

    activation_url = settings.CONFIRMATION_URL + token

    return activation_url

def build_reset_url(token):
    """
    Build the activation token URL
    """
    changepassword_url = settings.RESET_URL + token

    return changepassword_url

def send_activation_token(token_pk):
    """
    Send activation token by email
    """
    template = settings.TOKEN_ACTIVATION_EMAIL_BODY
    mail_subject = settings.TOKEN_ACTIVATION_EMAIL_SUBJECT
    token = Token.objects.get(pk = token_pk)
    tokenvalue = token.token
    activation_url = build_confirmation_url(token.token)
    emailto = token.externalMail
    message = render_to_string(template, {'name' : token.username, 'email': emailto, 'token': activation_url})
    email = EmailMessage(mail_subject, message, to=[emailto], from_email = settings.EMAIL_HOST_USER)
    email.send()

def send_reset_token(token_pk):
    """
    Send activation token by email
    """
    template = settings.TOKEN_RESET_EMAIL_BODY
    mail_subject = settings.TOKEN_RESET_EMAIL_SUBJECT
    token = Token.objects.get(pk = token_pk)
    tokenvalue = token.token
    reset_url = build_reset_url(token.token)
    emailto = token.externalMail
    message = render_to_string(template, {'name' : token.username, 'token': reset_url})
    email = EmailMessage(mail_subject, message, to=[emailto], from_email = settings.EMAIL_HOST_USER)
    email.send()
