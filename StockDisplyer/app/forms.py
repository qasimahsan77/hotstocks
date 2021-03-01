"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class Signup(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=True)
    last_name=forms.CharField(max_length=30,required=True)
    email=forms.EmailField(max_length=254,required=True)
    username=forms.CharField(max_length=50,required=True)
    password1=forms.CharField(widget=forms.PasswordInput(),required=True)
    password2=forms.CharField(widget=forms.PasswordInput(),required=True)
    class Mate:
        model=User
        fields=('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    pass