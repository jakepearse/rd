from django import forms
import datetime
from django.contrib import admin
from events.models import Promotion,Event,Ticket
from site_framework.admin import CommonMedia


class PromotionAdminForm(forms.ModelForm):
  class Meta:
    model = Promotion
  weekday = forms.IntegerField(help_text="""Use a number for the weekday 1 = Monday, 7 = Sunday.
  This prevents accidentaly adding tickets 
  for events on dates that dont match the correct weekday. 
  If an event can occur on any given weekday use 0 (zero)""")

class PromotionAdmin(admin.ModelAdmin):
  form = PromotionAdminForm
  #list_display=('id',)
  
class EventAdminForm(forms.ModelForm):
  ### This form allows vaidation of the date against the weekday specified
  ### in the related Promotion object.
  class Meta:
    model = Event
  def clean_date(self):
    testdate = datetime.datetime.strptime(self.data['date'],'%Y-%m-%d')
    isoday = testdate.isoweekday()
    promotion_qs = Promotion.objects.get(id=self.data['promotion'])
    parent_day = promotion_qs.weekday
    
    if isoday != parent_day and parent_day != 0:
      raise forms.ValidationError('The date does not match the promotion weekday')
    return self.cleaned_data['date']


class EventAdmin(admin.ModelAdmin):
  form = EventAdminForm
  list_display=('id','promotion','date',)
  list_filter=('promotion','date',)
  

class TicketAdmin(admin.ModelAdmin):
  list_display=['id','event','status','quantity','st_RefNumber',]
  list_filter=('event__date','event__promotion','status',)
  search_fields=['first_name','last_name','email',]
  raw_id_field = 'event'


### Now register with the admin site
admin.site.register(Promotion,PromotionAdmin,Media=CommonMedia,)
admin.site.register(Event,EventAdmin)
admin.site.register(Ticket,TicketAdmin,)
