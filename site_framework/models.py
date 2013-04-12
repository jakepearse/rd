from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Image(models.Model):
  ImageFile=models.ImageField(upload_to='articles',blank=True)
  def __unicode__(self):
    return "/static/uploads/%s"%(self.ImageFile)

class Article(models.Model):
  title=models.CharField(max_length=200)
  body=models.TextField()
  image=models.ForeignKey(Image,blank=True,null=True)
  author=models.ForeignKey(User)
  publishedDate=models.DateField()
  active=models.BooleanField()
  front_page=models.BooleanField()
  showTitle=models.BooleanField(default=True)
  def __unicode__(self):
    return self.title

