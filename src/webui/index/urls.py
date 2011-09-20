from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.index.views',
	url(r'^index/', 'index', name="index"),
	url(r'^credits/', 'credits', name="credits"),
	url(r'', 'index', name="main_kermit"),
)

