from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage
from events.models import Ticket, Event
import datetime

class Command(BaseCommand):
  args ='<emailaddress emailaddress ..>'  
  help = 'Closes the specified poll for voting'
  def handle(self, *args, **options):
    today = datetime.date.today()
    try:
      ticketQS = Ticket.objects.filter(event__date=today)
    except Event.DoesNotExist:
      raise CommandError('no tickets for %s' % today)
    headers='"order_ref","first_name",last_name","postcode","eventDate","quantity"'
    ticket_list =[]
    mail_string =""
    for ticket in ticketQS:
      ticket_list.append('"%s","%s","%s","%s","%s","%s"\n'%(ticket.id,ticket.first_name,ticket.last_name,ticket.postcode,ticket.event.date,ticket.quantity))
    for i in ticket_list:
      self.stdout.write(i)
      mail_string +=i
    recipients =[i for i in self.args]
    mail = EmailMessage("door-list for %s"%today, ".csv attached", "ticket-list", recipients)
    mail.attach('%s.csv'%today, mail_string, 'text/csv')
    mail.send()
