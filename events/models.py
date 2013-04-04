from django.db import models
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
  flyer=models.ImageField(upload_to="images/promotions/flyers",default="rollerdisco.png")
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
  user=models.ForeignKey(User)
  quantity=models.IntegerField()
  status=models.CharField(max_length=25)
  stResponse=models.CharField(max_length=255,null=True)
  
  def __unicode__(self):
    return "%s %s"%(self.user,self.event)
  
