import datetime, urllib, urllib2#, hashlib
from django.contrib.auth import authenticate,login
from django.shortcuts import HttpResponse, render_to_response, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.mail import send_mail
from forms import ticket_quantity, st_submit
from django import forms
from models import Ticket, Event, Promotion
from navigation.views import navlist
from django.views.decorators.csrf import csrf_exempt

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
  today = datetime.date.today()
  events = Event.objects.filter(promotion__id=promotion_id).order_by('date').filter(date__gte=today).filter(on_sale=True)
  return render_to_response('event_detail.html',
                              {'promotion':promotion,
                              'events':events,
                              'nav_list':nav_list,
                              'promotions':promotion_qs,})


def buytickets(request,event_id):
  event_id = event_id
  event = Event.objects.get(id=event_id)
  ticket_qs = Ticket.objects.filter(event__id=event_id).exclude(status='pending')
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
      event_date = str(event.date)
      #hash_string="r0LleRst8r"
      #securityHashObj = hashlib.new("sha256")
      #securityHashObj.update("%s%s%s%s%s"%('GBP','%.2f'%(order_value),str(new_ticket.id),'event27112',hash_string))
      #hash_value = 'g' + securityHashObj.hexdigest()
      newform = st_submit(initial={'currencyiso3a': 'GBP',
                      'mainamount':'%.2f'%(order_value),
                      'sitereference':'event27112',
                      'version':'1',
                      'orderreference':str(new_ticket.id),
                      'eventDate':event_date,
                      'quantity':ordered_tickets})
      return render_to_response('buytickets.html',{'nav_list':nav_list,'newform':newform,
        'ordered':ordered_tickets,
        'value':order_value,
        'event':event,
        'ticket':new_ticket,
        'promotions':promotion_qs},context_instance=RequestContext(request))
    #if the form is not valid
    else:
      return render_to_response('buytickets.html',
      {'nav_list':nav_list,
      'event':event,
      'tickets':remaining_tickets,
      'promotions':promotion_qs,
      'form':form}
      ,context_instance=RequestContext(request))
  #if form has not been POSTed
  else:
    form = ticket_quantity(initial={'event':event_id,
                          'value':event.promotion.price})
    return render_to_response('buytickets.html',
    {'nav_list':nav_list,
    'event':event,
    'tickets':remaining_tickets,
    'promotions':promotion_qs,
    'form':form}
    ,context_instance=RequestContext(request))

@csrf_exempt
def callback(request):
  admin_mail ="tickets@rollerdisco.com"
  if request.method == 'POST':
    data = request.POST
    results={'authcode':data['authcode'],
    'billing_email':data['billingemail'],
    'first_name':data['billingfirstname'],
    'last_name':data['billinglastname'],
    'postcode':data['billingpostcode'],
    'name_prefix':data['billingprefixname'],
    'telephone':data['billingtelephone'],
    'error_code':data['errorcode'],
    'main_amount':data['mainamount'],
    'order_reference':data['orderreference'],
    'status':data['status'],
    'transaction_reference':data['transactionreference'],
    'eventDate':data['eventDate'],
    'quantity':data['quantity']}
    ticket_ref = data['orderreference']
    #print ticket_ref
    try:
      ticket=Ticket.objects.filter(id=ticket_ref)
      ticket.first_name = results['first_name']
      ticket.last_name=results['last_name']
      ticket.name_prefix=results['name_prefix']
      ticket.telephone=results['telephone']
      ticket.postcode=results['postcode']
      ticket.email=results['billing_email']
      ticket.st_authCode=results['authcode']
      ticket.st_SecurityResponseCode='WTS'
      ticket.st_RefNumber=results['transaction_reference']
      ticket.st_ErrorCode=results['error_code']
      if results['error_code']==0 or '0':
        ticket.status="confirmed"
      else:
        ticket.status="error"
      ticket.save()
    except:
      rawdate = results['eventDate']
      datelist = rawdate.split('-')
      fixed_date = datetime.date(int(datelist[0]),int(datelist[1]),int(datelist[2]))
      matchedEvent = Event.objects.filter(date=fixed_date)
      ticket = Ticket(first_name=results['first_name'],
      last_name=results['last_name'],
      name_prefix=results['name_prefix'],
      telephone=results['telephone'],
      postcode=results['postcode'],
      email=results['billing_email'],
      st_authCode=results['authcode'],
      st_SecurityResponseCode='WTS',
      st_RefNumber=results['transaction_reference'],
      st_ErrorCode=results['error_code'],
      totalCost=results['main_amount'],
      quantity=results['quantity'],
      status="callback failed",
      event=matchedEvent[0])
      ticket.save()
    subject = "Ticket callback recived"
    somestring =""
    for k,v in results.items():
      somestring += "%s = %s\n"%(k,v)
    recipients = [admin_mail]
    sender="callback"
    try:
      send_mail(subject, somestring, sender, recipients)
    except:
      return HttpResponse('failing at first send_mail')
    customerSubject ="Your Rollerdisco Ticket"
    customerRecipients=['%s'%results['billing_email'],admin_mail]
    customerMailBody= "Ticket Number: %s\nCustomer Name: %s %s\n Date: %s\nPrice: %s\nLocation: Vauxhall\nTicket Type: RollerDisco"%(ticket_ref,
    results['first_name'],results['last_name'],results['eventDate'],results['main_amount'])
    try:
      send_mail(customerSubject,customerMailBody,'tickets@rollerdisco.com',customerRecipients)
    except:
      return HttpResponse('failing at 2nd send_mail')
    #return HttpResponse(200)
    return render_to_response('callback.html',{'data':results})
  else:
    return HttpResponse(404)

def clear_tickets(request,ticket_id):
  ticket_id=int(ticket_id)
  bad_ticket = Ticket.objects.get(id=ticket_id)
  bad_ticket.delete()
  return redirect('showevents')
