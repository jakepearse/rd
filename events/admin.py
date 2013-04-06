from django.contrib import admin
from events.models import Promotion,Event,Ticket

class TicketAdmin(admin.ModelAdmin):
  list_display=('id','event','user','status','quantity','stRefNumber')

admin.site.register(Promotion,)
admin.site.register(Event)
admin.site.register(Ticket,TicketAdmin)
