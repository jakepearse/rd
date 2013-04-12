from django import forms
from django.core import validators

class ContactForm(forms.Form):
  name = forms.CharField(label="Enter your Name", max_length=100)
  sender = forms.EmailField(label="Email Address *", required=True)
  subject = forms.CharField(label="Message Subject", required=False)
  message = forms.CharField(label="Enter your Message *", widget=forms.Textarea,required=True)
  email_copy = forms.BooleanField(label="E-mail a copy of this message to your own address.", required=False)