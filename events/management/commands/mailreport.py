from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage
from events.models import Ticket, Event
import datetime

class Command(BaseCommand):
  args ='<emailaddress emailaddress ..>'  
  help = 'generate and mail a ticket report'
  def handle(self, *args, **options):
    today = datetime.date.today()
    time = datetime.datetime.now()
    try:
      ticketQS = Ticket.objects.filter(event__date=today).filter(status='confirmed')
    except:
      raise CommandError('no event for %s' % today)
    with open('%s.csv'%time,'w') as file:
      file.write('"order_ref","first_name",last_name","postcode","eventDate","quantity"\n')
      for ticket in ticketQS:
        file.write('"%s","%s","%s","%s","%s","%s"\n'%(ticket.id,ticket.first_name,ticket.last_name,ticket.postcode,ticket.event.date,ticket.quantity))
    recipients =[i for i in self.args]
    mail = EmailMessage("door-list for %s"%today, "%s.csv attached"%time, "ticket-list", recipients)
    mail.attach_file(path="%s.csv"%time,mimetype="text/csv")
    mail.send()
