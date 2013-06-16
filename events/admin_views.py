from events.models import Ticket, Event
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, EmailMessage
from forms import ticket_report_form
import datetime

def ticket_report(request):
  today = datetime.date.today()
  event_list= Event.objects.all().filter(date__gte=today)
  form = ticket_report_form()
  if request.method =='POST':
    ticket_list = Ticket.objects.filter(event=request.POST['event']).filter(status='confirmed')
    total =0
    for i in ticket_list:
      total += i.quantity
    if request.POST['mailto']=='1':
      now = str(datetime.datetime.now())
      with open("/home/jake/rollerdisco/%s's-TicketReport for %s - %s.csv"%(user,request.POST['event'],now),'w') as report:
        report.write("'First Name','Last Name','Postcode','Quantity'")
        for ticket in ticket_list:
          report.write("'%s','%s','%s','%s'"%(ticket.first_name,ticket.last_name,ticket.postcode,ticket.quantity))
        report.write("'','','Total','%s'"%total)
      user = User.objects.get(id=request.POST['mailto'])
      recipients = ['%s'%user.email,]
      mail = EmailMessage("Your Ticket Report", "Automatically Generated", "noreply@rollerdisco.com", recipients)
      mail.attach_file(path="/home/jake/%s's-TicketReport for %s - %s.csv"%(user,request.POST['event'],now),mimetype="text/csv")
      mail.send()
    return render_to_response('admin/ticket_report.html', {'ticket_list':ticket_list,'form':form,'event_list':event_list,'total':total},RequestContext(request, {}),)
  else:
    return render_to_response('admin/ticket_report.html',{'form':form,'event_list':event_list}, RequestContext(request, {}))

ticket_report = staff_member_required(ticket_report) 
