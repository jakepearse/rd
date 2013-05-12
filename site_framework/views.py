from models import Article
from django.shortcuts import render_to_response, redirect
from navigation.views import navlist
from events.models import Promotion
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.core.mail import send_mail
from forms import ContactForm

nav_list = navlist()
promotion_qs = Promotion.objects.filter(active=True)
form = ContactForm()

def frontpage(request):
  url=request.path
  if url == '/':
    front_page_articles = Article.objects.filter(front_page=True).filter(active=True).order_by("-publishedDate")
    return render_to_response("front_page.html",{'articles':front_page_articles,'nav_list':nav_list,'promotions':promotion_qs,'url':url})
  elif url == '/contact/':
    return render_to_response("contact.html",{'form':form, 'nav_list':nav_list,'url':url,'promotions':promotion_qs},context_instance=RequestContext(request))
  elif url == '/find/': 
    return render_to_response("find.html",{'nav_list':nav_list,'url':url,'promotions':promotion_qs,})
  elif url =='/news/':
    articles_qs= Article.objects.filter(front_page=False).filter(active=True)
    return render_to_response('news.html',{'articles':articles_qs,'promotions':promotion_qs,'nav_list':nav_list,'url':url,})
    
def thankyou(request):
	if request.method == 'POST': 
  		form = ContactForm(request.POST)
  		if form.is_valid():
			name = form.cleaned_data['name']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			email_copy = form.cleaned_data['email_copy']
			recipients = ['mail@jakepearse.com']
			if email_copy == 1:
				recipients.append(sender)
			send_mail(subject, message, sender, recipients)
			return render_to_response('thanks.html',{'nav_list':nav_list, 'promotions':promotion_qs,})
	else:
		form = ContactForm()
		return render_to_response("contact.html",{'form':form, 'nav_list':nav_list,'url':url,'promotions':promotion_qs},context_instance=RequestContext(request))
