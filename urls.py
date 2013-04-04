from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'site_framework.views.frontpage', name='home'),
	# url(r'^rollerdisco/', include('rollerdisco.foo.urls')),
  #url(r'^adduser','events.views.adduser',name="newuser"),
  #url(r'^showtickets/$','events.views.showtickets', name="index"),
	#url(r'^addticket/', 'events.views.addticket', name="newticket"),
	url(r'^showevents/$', 'events.views.showevents'),
  url(r'^showevents/(.*)/eventdetail$', 'events.views.eventdetail'),
  url(r'^navigation/$', 'navigation.views.navlist'),
  # Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	 url(r'^admin/', include(admin.site.urls)),
)
