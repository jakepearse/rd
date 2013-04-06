from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'site_framework.views.frontpage', name='home'),
	url(r'^contact/$', 'site_framework.views.frontpage'),
	url(r'^find/$', 'site_framework.views.frontpage'),
	# url(r'^rollerdisco/', include('rollerdisco.foo.urls')),
	url(r'^adduser','events.views.register',name='adduser'),
	url(r'^testlogin/$','events.views.register',name='adduser'),
	url(r'^showevents/$', 'events.views.showevents'),
	url(r'^showevents/(.*)/eventdetail$', 'events.views.eventdetail'),
	url(r'^navigation/$', 'navigation.views.navlist'),
	url(r'^buytickets/(.*)/$', 'events.views.buytickets', name='buytickets'),
  url(r'^adduser/$', 'events.views.register', name='register'),
  url(r'^submit_order/$', 'events.views.submit_order', name='submit_order'),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	 url(r'^admin/', include(admin.site.urls)),
)
