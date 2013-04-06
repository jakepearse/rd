import datetime
from django.contrib.auth import authenticate,login
from django.shortcuts import HttpResponse, render_to_response, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.mail import send_mail
from forms import RegistrationForm, ticket_quantity, confirm_order
from django import forms
from models import Ticket, Event, Promotion
from navigation.views import navlist

nav_list = navlist()
promotion_qs = Promotion.objects.filter(active=True)

def testlogin(request,event_id):
  form = RegistrationForm()
  event_id = int(event_id)
  event = Event.objects.get(id=event_id)
  if request.user.is_authenticated():
    return render_to_response('buytickets.html', {'has_account': True,'event':event})
  else:
    return redirect('adduser.html',{'event':event,'form':form,'promotions':promotion_qs},context_instance=RequestContext(request))
    
def register(request,event):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('buytickets.html', {'has_account': True,'event':event})
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
        user.active = True
        user.save()
        newuser = authenticate(username=username, password=password)
        if newuser.is_active:
          login(request, newuser)
          return redirect('buytickets.html',{'has_account':True,'event':event})
      else:
        return render_to_response('adduser.html',{'form':form,'event':event},context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
    return render_to_response('adduser.html',{'form':form,'event':event},context_instance=RequestContext(request))
    
def showtickets(request):
  ticket_list = Ticket.objects.all()
  return render_to_response('ticketlist.html',{'ticket_list':ticket_list})
  
def showevents(request):
  active_promotion_list = Promotion.objects.filter(active=True)
  event_list = Event.objects.filter(promotion__active=True)
  return render_to_response('event_list.html',{'promotions':active_promotion_list,'event_list':event_list,'nav_list':nav_list})
  
def eventdetail(request,promotion_id):
  promotion_id = int(promotion_id)
  promotion = Promotion.objects.get(id=promotion_id)
  events = Event.objects.filter(promotion__id=promotion_id)
  return render_to_response('event_detail.html',{'promotion':promotion,'events':events,'nav_list':nav_list,'promotions':promotion_qs,})

def buytickets(request,event_id):
  #get event form url
  event_id = int(event_id)
  event = Event.objects.get(id=event_id)
  #find any tickets sold for that event
  ticket_qs = Ticket.objects.filter(event__id=event_id)
  #count the tickets
  tickets_sold = 0
  for i in ticket_qs:
    tickets_sold += int(i.quantity)
  remaining_tickets = int(event.promotion.ticketAllowance) - tickets_sold
  #dont let the total fall below 0
  if remaining_tickets < 0:
    remaining_tickets = 0
  #if the form is POSTed
  if request.method == 'POST':
    form = ticket_quantity(request.POST)
    #check the form is valid
    if form.is_valid():
      cd = form.cleaned_data
      ordered_tickets = cd.get('quantity')
      order_value = event.promotion.price * ordered_tickets
      # return the quantity and value of order
      form = confirm_order(initial={'event':int(event.id),'quantity':int(ordered_tickets),'value':int(order_value)})
      return render_to_response('buytickets.html',{'value':order_value,
      'form':form,
      'ordered':ordered_tickets,
      'event':event,
      'promotions':promotion_qs}
      ,context_instance=RequestContext(request))
    #if the form is not vailid
    else:
      return render_to_response('buytickets.html',{'event':event,'tickets':remaining_tickets,'promotions':promotion_qs,'form':form},context_instance=RequestContext(request))
  #if form has not been POSTed
  else:
    form = ticket_quantity()
    return render_to_response('buytickets.html',{'event':event,'tickets':remaining_tickets,'promotions':promotion_qs,'form':form},context_instance=RequestContext(request))

def submit_order(request):
  form = confirm_order(request.POST)
  if form.is_valid():
    cd = form.cleaned_data
    event = Event.objects.get(id=cd.get('event'))
    quantity = int(cd.get('quantity'))
    value = int(cd.get('value'))
    new_ticket = Ticket(event=event,
                        quantity=quantity,
                        totalCost=value)
    new_ticket.save()
    return HttpResponse('ok')
  else:
    return HttpResponse('fail')
      
      
