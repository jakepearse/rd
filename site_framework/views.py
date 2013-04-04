from models import Article
from django.shortcuts import render_to_response, redirect
from navigation.views import navlist
# Create your views here.

nav_list = navlist()

def frontpage(request):
  front_page_articles = Article.objects.filter(front_page=True)
  return render_to_response("front_page.html",{'articles':front_page_articles,'nav_list':nav_list})
