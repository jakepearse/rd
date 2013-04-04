from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
  title=models.CharField(max_length=200)
  body=models.TextField()
  author=models.ForeignKey(User)
  publishedDate=models.DateField()
  active=models.BooleanField()
  front_page=models.BooleanField()
  def __unicode__(self):
    return self.title
