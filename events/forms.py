from django import forms
from django.core import validators
from models import Ticket, Event
from django.contrib.auth.models import User
import datetime
from django.forms.extras.widgets import SelectDateWidget


class ticket_quantity(forms.Form):
  quantity = forms.IntegerField(required=True,label="Number of tickets",min_value=1,max_value=25,help_text="Limit of 25 tickets per customer")
  email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'align':'left'}),label="Email Address",help_text="Your e-ticket will be delivered to this address")
  c_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'align':'left'}),label="confirm your email address")
  postcode = forms.CharField(required=True,widget=forms.TextInput(attrs={'align':'left'}),label="UK Postcode")
  tel= forms.CharField(required=True,widget=forms.TextInput(attrs={'align':'left'}),label="Contact telephone number")
  event= forms.CharField(widget=forms.HiddenInput())
  value=forms.CharField(max_length=10,widget=forms.HiddenInput())
  def clean(self):
    clean_data=self.cleaned_data
    order_quantity = clean_data.get('quantity')
    event_id = self.data['event']
    ticket_qs = Ticket.objects.filter(event=event_id).exclude(status='pending')
    sold_tickets=0
    for i in ticket_qs:
        sold_tickets += i.quantity
    remaining_tickets = Event.objects.get(id=event_id).promotion.ticketAllowance - sold_tickets
    if order_quantity > remaining_tickets:
      raise forms.ValidationError('Not enough tickets in stock!')
    email=clean_data.get("email")
    cemail=clean_data.get("c_email")
    if email != cemail:
        raise forms.ValidationError(u'Email addreses do not match!')    
    return clean_data


class st_submit(forms.Form):
  currencyiso3a = forms.CharField(max_length=3,widget=forms.HiddenInput())
  mainamount = forms.CharField(max_length=4,widget=forms.HiddenInput())
  sitereference = forms.CharField(max_length=20,widget=forms.HiddenInput())
  version = forms.CharField(max_length=1,widget=forms.HiddenInput())
  orderreference = forms.CharField(max_length=255,widget=forms.HiddenInput())
  eventDate = forms.CharField(max_length=255,widget=forms.HiddenInput())
  quantity = forms.CharField(max_length=255,widget=forms.HiddenInput())
  #sitesecurity = forms.CharField(max_length=255)

class ticket_report_form(forms.Form):
  eventQS=Event.objects.all()
  userQS=User.objects.all()
  event = forms.ModelChoiceField(queryset=eventQS)
  mailto = forms.ModelChoiceField(queryset=userQS)
