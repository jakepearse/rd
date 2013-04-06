from models import Article
from django.shortcuts import render_to_response, redirect
from navigation.views import navlist
from events.models import Promotion
# Create your views here.

nav_list = navlist()
promotion_qs = Promotion.objects.filter(active=True)

def frontpage(request):
  url=request.path
  if url == '/':
    front_page_articles = Article.objects.filter(front_page=True).order_by("publishedDate")
    return render_to_response("front_page.html",{'articles':front_page_articles,'nav_list':nav_list,'promotions':promotion_qs,'url':url})
  elif url == '/contact/':
    return render_to_response("contact.html",{'nav_list':nav_list,'url':url,'promotions':promotion_qs,})
  elif url == '/find/': 
    return render_to_response("find.html",{'nav_list':nav_list,'url':url,'promotions':promotion_qs,})
