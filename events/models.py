from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
# hello i am prakash
class Promotion(models.Model):
  title=models.CharField(max_length=200)
  weekday=models.CharField(max_length=9,null=True)
  startTime=models.TimeField(auto_now=False)
  finishTime=models.TimeField(auto_now=False)
  price=models.DecimalField(max_digits=4,decimal_places=2)
  ticketAllowance=models.IntegerField()
  ageRestriction=models.IntegerField()
  flyer=models.ImageField(upload_to="static/images/upload",default="static/images/rollerdisco_logo_thumb.png")
  active=models.BooleanField()
  def __unicode__(self):
    return self.title

class Event(models.Model):
  date=models.DateField()
  promotion=models.ForeignKey(Promotion)
  def __unicode__(self):
    return "%s %s"%(self.date,self.promotion.title)

class Ticket(models.Model):
  event=models.ForeignKey(Event)
  user=models.ForeignKey(User,null=True)
  quantity=models.IntegerField()
  totalCost=models.IntegerField()
  status=models.CharField(max_length=25,default='pending')
  stResponseCode=models.CharField(max_length=255,null=True)
  stRefNumber=models.CharField(max_length=255,null=True)
  stResponseText=models.CharField(max_length=255, null=True)
  orderPlaced=models.DateTimeField(default=datetime.datetime.now())
  def __unicode__(self):
    return "%s %s %s"%(self.user,self.event,self.status)
  
