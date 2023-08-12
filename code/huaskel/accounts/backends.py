from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from huaskel import settings


import logging
UserModel = get_user_model()
logger = logging.getLogger('huaskel')



class EmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        logger.debug('User %s attempting to login' %username)

        if username.endswith(settings.AUTH_LDAP_INTERNAL_DOMAIN):
            logger.debug('User %s is an internal user, deffering to LDAP auth' %username)
            return

        try:
            user = UserModel.objects.get( email = username )
            logger.debug('User %s exists' %username)

        except UserModel.DoesNotExist:
            logger.debug('User %s does not exist' %username)
            return

        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter( Q(email__iexact=username) ).order_by('id').first()
            logger.debug('There are multiple users with the username %s' %username)

        if user.check_password(password) and self.user_can_authenticate(user):
            logger.info('User %s was successfully authenticated' %username)
            return user
        else:
            logger.info('User %s was NOT successfully authenticated' %username)
