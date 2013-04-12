import datetime, urllib, urllib2
from django.contrib.auth import authenticate,login
from django.shortcuts import HttpResponse, render_to_response, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.mail import send_mail
from forms import RegistrationForm, ticket_quantity, st_submit
from django import forms
from models import Ticket, Event, Promotion
from navigation.views import navlist

# The nav_list query set from the navigation app provides the list to go
# in the navigation tabs, you should pass 'nav_list':nav_list to
# anything that renders through a template which includes "base.html"
# ie. everything. 
nav_list = navlist()

# The promotion query set provides all the active promotions to populate
# the left side bar, you should pass 'promotions':promotion_qs to anything
# that renders through a template which includes "base.html"
# Yes! that would be everything!
promotion_qs = Promotion.objects.filter(active=True)

    
def showtickets(request):
  # TODO: Remove this view, I think its useless.
  ticket_list = Ticket.objects.all()
  return render_to_response('ticketlist.html',{'ticket_list':ticket_list})

  
def showevents(request):
  # This is the main view for the show events url pattern,
  # for clarity it would better be named showpromotions
  # It's named showevents for lazy-ass legacy compatiblity.
  active_promotion_list = Promotion.objects.filter(active=True)
  event_list = Event.objects.filter(promotion__active=True)
  return render_to_response('event_list.html',
                              {'promotions':active_promotion_list,
                              'event_list':event_list,
                              'nav_list':nav_list})

  
def eventdetail(request,promotion_id):
  # Should be called promotiondetail for similar reasons
  promotion_id = int(promotion_id)
  promotion = Promotion.objects.get(id=promotion_id)
  events = Event.objects.filter(promotion__id=promotion_id)
  return render_to_response('event_detail.html',
                              {'promotion':promotion,
                              'events':events,
                              'nav_list':nav_list,
                              'promotions':promotion_qs,})


def buytickets(request,event_id):
  event_id = event_id
  event = Event.objects.get(id=event_id)
  ticket_qs = Ticket.objects.filter(event__id=event_id)
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
      event = Event.objects.get(id=cd.get('event'))
      new_ticket = Ticket(event=event,
        quantity=ordered_tickets,
        totalCost=order_value)
      new_ticket.save()
      event_id = str(event.id)
      hash_value ='hello i am a hash value'
      newform = st_submit(initial={'currencyiso3a': 'GBP',
                      'mainamount':str(order_value),
                      'sitereference':'test_event32549',
                      'version':'1',
                      'orderreference':new_ticket.id,
                      'sitesecurity':hash_value})
      return render_to_response('buytickets.html',{'newform':newform,
        'ordered':ordered_tickets,
        'value':order_value,
        'event':event,
        'ticket':new_ticket,
        'promotions':promotion_qs},context_instance=RequestContext(request))
    #if the form is not vailid
    else:
      return render_to_response('buytickets.html',
      {'event':event,
      'tickets':remaining_tickets,
      'promotions':promotion_qs,
      'form':form}
      ,context_instance=RequestContext(request))
  #if form has not been POSTed
  else:
    form = ticket_quantity(initial={'event':event_id,
                          'value':event.promotion.price})
    return render_to_response('buytickets.html',
    {'event':event,
    'tickets':remaining_tickets,
    'promotions':promotion_qs,
    'form':form}
    ,context_instance=RequestContext(request))

      
def callback(request):
  if request.method == 'POST':
    data = request.POST
    results={
    'authcode':data.get('authcode'),
    'billing_email':data.get('billingemail'),
    'first_name':data.get('billingfirstname'),
    'last_name':data.get('billinglastname'),
    'postcode':data.get('billingpostcode'),
    'name_prefix':data.get('billingprefixname'),
    'telephone':data.get('billingtelephone'),
    'error_code':data.get('errorcode'),
    'main_amount':data.get('mainamount'),
    'order_reference':data.get('orderreference'),
    'security_response_code':data.get('securityresponsesecuritycode'),
    'status':data.get('status'),
    'transaction_reference':data.get('transactionreference')
    }
    ticket=Ticket.objects.get(id=data.get('orderreference'))
    ticket.first_name = results['first_name']
    ticket.last_name=results.get('last_name')
    ticket.postcode=results.get('postcode')
    return render_to_response('callback.html',{'data':results})
  return HttpResponse(404)

def clear_tickets(request,ticket_id):
  ticket_id=int(ticket_id)
  bad_ticket = Ticket.objects.get(id=ticket_id)
  bad_ticket.delete()
  return redirect('showevents')
  
