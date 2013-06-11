from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

#def valid_day(weekday,date_object):
    #if weekday != now(date_object):
      #raise ValidationError(u'Weekday %s does not match date!'%weekday)
      
      
class Promotion(models.Model):
  title=models.CharField(max_length=200)
  weekday=models.IntegerField()
  startTime=models.TimeField(auto_now=False)
  finishTime=models.TimeField(auto_now=False)
  price=models.DecimalField(max_digits=4,decimal_places=2)
  ticketAllowance=models.IntegerField()
  ageRestriction=models.IntegerField()
  flyer=models.ImageField(upload_to='flyers',default="static/images/rollerdisco_logo_thumb.png")
  description=models.TextField(null=True)
  active=models.BooleanField()
  def __unicode__(self):
    return self.title

class Event(models.Model):
  date=models.DateField()
  promotion=models.ForeignKey(Promotion)
  on_sale=models.BooleanField(default=1)
  def __unicode__(self):
    return "%s - %s "%(self.date,self.promotion.title)

class Ticket(models.Model):
  event=models.ForeignKey(Event)
  first_name=models.CharField(max_length=255,blank=True)
  last_name=models.CharField(max_length=255,blank=True)
  name_prefix=models.CharField(max_length=255,blank=True)
  telephone=models.CharField(max_length=255,blank=True)
  postcode=models.CharField(max_length=255,blank=True)
  email=models.EmailField(blank=True)
  st_authCode=models.CharField(max_length=255,blank=True)
  quantity=models.IntegerField()
  totalCost=models.IntegerField()
  status=models.CharField(max_length=25,default='pending')
  st_SecurityResponseCode=models.CharField(max_length=255,null=True,blank=True)
  st_RefNumber=models.CharField(max_length=255, blank=True)
  st_ErrorCode=models.CharField(max_length=255, blank=True)
  orderPlaced=models.DateTimeField(default=datetime.datetime.now())
  def __unicode__(self):
    return "%s, %s %s %s"%(self.last_name,self.first_name,self.event,self.status)
  
