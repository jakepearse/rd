from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'site_framework.views.frontpage', name='home'),
	url(r'^thankyou/$', 'site_framework.views.thankyou'),
	url(r'^contact/$', 'site_framework.views.frontpage', name='contact'),
	url(r'^find/$', 'site_framework.views.frontpage', name='location'),
	# url(r'^rollerdisco/', include('rollerdisco.foo.urls')),
	url(r'^showevents/$', 'events.views.showevents',name='showevents'),
	url(r'^showevents/(.*)/eventdetail$', 'events.views.eventdetail'),
	url(r'^navigation/$', 'navigation.views.navlist', name='navlist'),
	url(r'^buytickets/(.*)/$', 'events.views.buytickets', name='buytickets'),
  # Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
  url(r'^admin/', include(admin.site.urls)),
  url(r'^callback/$', 'events.views.callback', name='callback'),
  url(r'^cleartickets/(\d+)/$', 'events.views.clear_tickets'),
  ############ ADD NEW URL PATTERNS TO END OF FILE #####################
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
  url(r'^news/$','site_framework.views.frontpage',name='news'),
)
