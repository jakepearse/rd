import datetime
from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.mail import send_mail
from forms import RegistrationForm
from django import forms
from models import Ticket, Event, Promotion
from navigation.views import navlist

nav_list = navlist()
  
def register(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('buytickets.html', {'has_account': True})
    elif request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
        cd = form.cleaned_data
        #make a user here
        username = cd.get('username')
        firstname = cd.get('firstname')
        lastname = cd.get('lastname')
        email = cd.get('email')
        password = cd.get('password')
        user = User.objects.create_user(username,email,password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        user = authenticate(username=username, password=password)
        login(request,user)
        #return redirect('adduser')
      else:
        return render_to_response('adduser.html',{'form':form},context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
    return render_to_response('adduser.html',{'form':form},context_instance=RequestContext(request))
    
def showtickets(request):
  ticket_list = Ticket.objects.all()
  return render_to_response('ticketlist.html',{'ticket_list':ticket_list})
  
def showevents(request):
  active_promotion_list = Promotion.objects.filter(active=True)
  event_list = Event.objects.filter(promotion__active=True)
  return render_to_response('event_list.html',{'promotions':active_promotion_list,'event_list':event_list,'nav_list':nav_list})
  
def eventdetail(request,event_id):
  event = Event.objects.get(id=event_id)
  ticket_qs = Ticket.objects.filter(event__id=event_id)
  tickets_sold = 0
  for i in ticket_qs:
    tickets_sold += int(i.quantity)
  remaining_tickets = int(event.promotion.ticketAllowance) - tickets_sold
  return render_to_response('event_detail.html',{'event':event,'nav_list':nav_list,'tickets_available':remaining_tickets})
