from django.core.management.base import BaseCommand, CommandError
from events.models import Event
import datetime

class Command(BaseCommand):
  args =""  
  help = 'Closes the specified poll for voting'
  def handle(self, *args, **options):
    today = datetime.date.today()
    try:
      eventQS = Event.objects.filter(date=today).filter(promotion__title='Family Jam')
    except Event.DoesNotExist:
      raise CommandError('no event for %s' % today)
    for event in eventQS:
      event.on_sale = 0
      event.save()
      self.stdout.write('Successfully closed family jam event "%s"\n' % event)
