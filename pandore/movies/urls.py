from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

json_patterns = patterns('',
        url(r'^details/(?P<pk>\d+)/$', 'movies.json.details'),
        )

urlpatterns = patterns('',
    url(r'^json/', include(json_patterns)),
    )
