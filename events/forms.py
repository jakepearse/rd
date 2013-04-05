from django import forms
from django.core import validators
from models import Ticket
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
  username = forms.CharField(max_length=50)
  firstname = forms.CharField()
  lastname = forms.CharField()
  email = forms.EmailField(label='your email address')
  password = forms.CharField(widget=forms.PasswordInput,label="create a password")
  password2 = forms.CharField(widget=forms.PasswordInput,label="confirm password")

  def clean_username(self):
    username = self.cleaned_data['username']
    olduser = User.objects.filter(username=username)
    if olduser:
      raise forms.ValidationError('Username exists')
    return username
  
  def clean_password(self):
    password = self.cleaned_data['password']
    password2 = self.data['password2']
    if password != password2:
      raise forms.ValidationError('Passwords do not match')
    return password
