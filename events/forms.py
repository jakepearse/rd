from django.forms import ModelForm
from models import Ticket
from django.contrib.auth.models import User
class TicketForm(ModelForm):
  class Meta:
    model = Ticket
    
class UserForm(ModelForm):
  class Meta:
    model = User
