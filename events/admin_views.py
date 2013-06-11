from events.models import Ticket, Event
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from forms import ticket_report_form

def ticket_report(request):
  event_list= Event.objects.all()
  if request.method =='POST':
    ticket_list = Ticket.objects.filter(event=request.POST['event']).filter(status='confirmed')
    return render_to_response('admin/ticket_report.html', {'ticket_list':ticket_list,'form':ticket_report_form,'event_list':event_list},RequestContext(request, {}),)
  else:
    return render_to_response('admin/ticket_report.html',{'form':ticket_report_form,'event_list':event_list}, RequestContext(request, {}))

ticket_report = staff_member_required(ticket_report) 
