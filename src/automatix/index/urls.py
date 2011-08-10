from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('automatix.index.views',
	url(r'^index/', 'index', name="index"),
	url(r'^credits/', 'credits', name="credits"),
	url(r'', 'index'),
)

