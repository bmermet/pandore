from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pandore.views.home', name='home'),
    # url(r'^pandore/', include('pandore.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Movie search
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^movies/', include('movies.urls', namespace='movies')),
    url(r'^series/', include('series.urls', namespace='series')),
)
