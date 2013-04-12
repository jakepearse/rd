from django.contrib import admin
from site_framework.models import Article, Image

class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    'admin/js/editor.js',
  )
  css = {
    'all': ('admin/css/editor.css',),
  }
  
admin.site.register(Article,
  title  = ('title',),
  search_fields = ['title',],
  Media = CommonMedia,)

admin.site.register(Image)
