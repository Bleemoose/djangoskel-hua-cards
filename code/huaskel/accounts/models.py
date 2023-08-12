from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    username = models.CharField(_('username'), max_length = 200, unique = True )
    email = models.EmailField(_('email address'), unique = True)
    title = models.CharField(_('title'), max_length = 200, default = 'None' )
    department = models.CharField(_('department'), max_length = 200, default = 'None' )


class TokenManager(models.Manager):

    # get all expired tokens
    def get_expired(self):
        return Token.objects.filter( expiration__lt = timezone.now() )

    # delete all expired tokens
    def delete_expired(self):
        expired_tokens = self.get_expired()
        for token in expired_tokens:
            token.delete()

class Token(models.Model):
    """
    model for token generators
    """
    token = models.CharField ( max_length = 200 )
    expiration = models.DateTimeField('expiration date' )
    externalMail = models.EmailField( max_length = 100 )
    username = models.CharField( max_length = 100 )
    type = models.CharField( max_length = 20, default = 'activation' )
    objects = TokenManager()

    def __str__(self):
        return "token %s used for %s belonging to user %s expires at %s" %(self.token,
                self.type, self.username, self.expiration)

    def has_expired(self):
        return self.expiration < timezone.now()
