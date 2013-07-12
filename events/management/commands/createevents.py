from django.core.management.base import BaseCommand, CommandError
from events.models import Promotion,Event
import datetime

class Command(BaseCommand):  
  help = 'create events for the next 30 days'
  def handle(self, *args, **options):
    base = datetime.date.today()
    dateList = [ base + datetime.timedelta(x) for x in range(0,60) ]
    for i in dateList:
      self.stdout.write(str(i) + 'isoweekday ='+str(+i.isoweekday()))
      if i.isoweekday() in [4,5,6]:
        self.stdout.write('iso wekkday hit')
        if Event.objects.filter(date=i):
          self.stdout.write(str(i) + ' event already exists\n')
          continue
        if i.isoweekday() == 4:
          self.stdout.write('hit something')
          p = Promotion.objects.get(title='Thursday Night')
          e = Event(date=i,promotion=p)
          e.save()
          self.stdout.write('created Event : ' + str(e) + '\n')
        elif i.isoweekday() == 5:
          p = Promotion.objects.get(title='Friday Night')
          e = Event(date=i,promotion=p)
          e.save()
          self.stdout.write('created Event : ' + str(e) + '\n')
        else:
          p = Promotion.objects.get(title='Saturday Night')
          e = e = Event(date=i,promotion=p)
          e.save()
          self.stdout.write('created Event : ' + str(e) + '\n')
          # make a family jam event
          p = Promotion.objects.get(title='Family Jam')
          e = e = Event(date=i,promotion=p)
          e.save()
          self.stdout.write('created Event : ' + str(e) + '\n')
