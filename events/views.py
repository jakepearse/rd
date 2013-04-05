import datetime
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import TicketForm, UserForm
from models import Ticket, Event, Promotion
from navigation.views import navlist

nav_list = navlist()
promotion_qs = Promotion.objects.filter(active=True)

def adduser(request):
  adduser_form = UserForm(request.POST or None)
  if adduser_form.is_valid():
    create_user = adduser_form.save()
    create_user.save()
    return redirect(addticket)
  return render_to_response('adduser_form.html',{'adduser_form':adduser_form},context_instance=RequestContext(request))
  
def addticket(request):
  addticket_form = TicketForm(request.POST or None)
  if addticket_form.is_valid():
    create_form = addticket_form.save()
    create_form.save()
    return redirect(showtickets)
  return render_to_response('addticket_form.html',{'addticket_form':addticket_form},context_instance=RequestContext(request))
  
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
  event_qs = Event.objects.filter(promotion__id=promotion_id)
 # tickets_sold = 0
 # for i in ticket_qs:
 #   tickets_sold += int(i.quantity)
 # remaining_tickets = int(event.promotion.ticketAllowance) - tickets_sold
  return render_to_response('event_detail.html',{'events':event_qs,'nav_list':nav_list,'promotion':promotion,'promotions':promotion_qs})

def find(request):
  url=request.path
  return render_to_response('find.html',{'promotions':promotion_qs,'nav_list':nav_list,'url':url})

def contact(request):
  url=request.path
  return render_to_response('contact.html',{'promotions':promotion_qs,'nav_list':nav_list,'url':url})
