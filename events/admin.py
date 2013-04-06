from django.contrib import admin
from events.models import Promotion,Event,Ticket

admin.site.register(Promotion,)
admin.site.register(Event)
admin.site.register(Ticket)
