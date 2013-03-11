from django.conf.urls import patterns, url
from haystack.views import SearchView
from movies.advanced_movie_search import AdvancedMovieSearchForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^autocomplete/', 'search.views.autocomplete', name='autocomplete'),
    url(r'^json/', 'search.json.search', name='json'),
    # Movie search
    url(r'.*', SearchView(
        template='search/search.html',
        form_class=AdvancedMovieSearchForm
        ), name='haystack.urls'),
    )
