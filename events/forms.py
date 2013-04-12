from django import forms
from django.core import validators
from models import Ticket, Event
from django.contrib.auth.models import User

class ticket_quantity(forms.Form):
  quantity = forms.IntegerField(label="Number of tickets",min_value=1,max_value=25,help_text="Limit of 25 tickets per customer")
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
