from django.shortcuts import render_to_response
from events.models import Promotion
# Create your views here.
def navlist(request=None):
  sections =('Home','Find Us','Photos','Contact')
  if not request:
    return sections
  else:
    return render_to_response('nav.html',{'nav_elements':sections})
