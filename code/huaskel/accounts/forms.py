from django import forms
from django.core.exceptions import ValidationError
from .passcomplexity import password_is_ok, password_policy

class externalMailField( forms.EmailField ):

    def validate(self, value):

        super().validate(value)
        if '@hua.gr' in value:
            raise ValidationError('Παρακαλούμε μην χρησιμοποιήσετε διεύθυνση @hua.gr')

class complexPassword( forms.CharField ):

    def validate(self, value):

        super().validate(value)
        if not password_is_ok(value):
            raise ValidationError(password_policy())

class extMailForm(forms.Form):
    """
    Form for external mail
    """
    email = externalMailField(required = True, label = 'Διεύθυνση ηλεκτρονικού ταχυδρομείου')

class forgotPasswordForm(forms.Form):
    """
    Form for forgot password
    """
    uid = forms.CharField(label = 'Όνομα χρήστη (χωρίς @hua.gr)')
    email = externalMailField(required = True, label = 'Διεύθυνση ηλεκτρονικού ταχυδρομείου')

class changePasswordForm(forms.Form):
    """
    Form for changing password
    """
    password1 = complexPassword(label='Εισάγετε τον νέο κωδικό', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Επιβεβαιώση του κωδικού', widget = forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Οι κωδικοί που δώσατε δεν ταιριάζουν, προσπαθήστε ξανά')

        return cleaned_data

class verifyPasswordForm(forms.Form):
    """
    Form for changing password
    """
    password = forms.CharField(label='Εισάγετε τον κωδικό σας', widget = forms.PasswordInput)
