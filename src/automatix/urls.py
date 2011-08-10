from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'automatix.views.home', name='home'),
    # url(r'^automatix/', include('automatix.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^restapi/', include('automatix.restserver.urls')),
    (r'^index/(.*)', include('automatix.index.urls')),
    (r'', include('automatix.index.urls')),
)
