from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

json_patterns = patterns('',
        url(r'^details/(?P<id_imdb>\d+)/$',
            'series.json.details_series', name='json-detail'),
        url(r'^details/(?P<series_id_imdb>\d+)/(?P<season_number>\d+)/?$',
            'series.json.details_season', name='json-detail-season'),
        url(r'^details/(?P<series_id_imdb>\d+)/(?P<season_number>\d+)/(?P<episode_number>\d+)/?$',
            'series.json.details_episode', name='json-detail-episode'),
        url(r'^search/', 'series.json.search', name='json-search')
        )

urlpatterns = patterns('',
    url(r'^json/', include(json_patterns)),
    )
