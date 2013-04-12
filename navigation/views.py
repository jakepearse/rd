from django.shortcuts import render_to_response
from events.models import Promotion
from django.utils.datastructures import SortedDict
# Create your views here.
def navlist(request=None):
  sections = SortedDict([
  ('Home','/'),
  ('Find Us','/find/'),
  ('News','/news/'),
  ('Photos',"http://rollerdisco.zenfolio.com/ target='blank'"),
  ('Contact','/contact/')])
  if not request:
    return sections
  else:
    return render_to_response('nav.html',{'nav_elements':sections})
