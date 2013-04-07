from django import forms
from django.core import validators
from models import Ticket, Event
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

class ticket_quantity(forms.Form):
  quantity = forms.IntegerField(label="Number of tickets",min_value=1)
  event= forms.CharField(widget=forms.HiddenInput())
  value=forms.CharField(max_length=10,widget=forms.HiddenInput())
  def clean_quantity(self):
    order_quantity = self.cleaned_data['quantity']
    event_id = self.data['event']
    ticket_qs = Ticket.objects.filter(event=event_id)
    sold_tickets = 0
    for i in ticket_qs:
      sold_tickets += i.quantity
    remaining_tickets = Event.objects.get(id=event_id).promotion.ticketAllowance - sold_tickets
    if order_quantity > remaining_tickets:
      raise forms.ValidationError('Not enough tickets in stock!')
    return order_quantity
      
class st_submit(forms.Form):
  currencyiso3a = forms.CharField(max_length=3,widget=forms.HiddenInput())
  mainamount = forms.CharField(max_length=4,widget=forms.HiddenInput())
  sitereference = forms.CharField(max_length=20,widget=forms.HiddenInput())
  version = forms.CharField(max_length=1,widget=forms.HiddenInput())
  orderreference = forms.CharField(max_length=255,widget=forms.HiddenInput())
  #sitesecurity = forms.CharField(max_length=255)
