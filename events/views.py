import datetime
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import TicketForm, UserForm
from models import Ticket, Event, Promotion
from navigation.views import navlist

nav_list = navlist()

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
  
def eventdetail(request,event_id):
  event = Event.objects.get(id=event_id)
  ticket_qs = Ticket.objects.filter(event__id=event_id)
  tickets_sold = 0
  for i in ticket_qs:
    tickets_sold += int(i.quantity)
  remaining_tickets = int(event.promotion.ticketAllowance) - tickets_sold
  return render_to_response('event_detail.html',{'event':event,'nav_list':nav_list,'tickets_available':remaining_tickets})
