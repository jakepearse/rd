from django.core.management.base import BaseCommand, CommandError
from events.models import Event
import datetime

class Command(BaseCommand):
  args =""  
  help = 'Closes the specified poll for voting'
  def handle(self, *args, **options):
    today = datetime.date.today()
    try:
      event = Event.objects.filter(date=today).exclude(promotion__title='Family Jam')
    except Event.DoesNotExist:
      raise CommandError('no event for %s' % today)
    event[0].on_sale = False
    event[0].save()
    self.stdout.write('Successfully closed event "%s"\n' % event[0].date)
