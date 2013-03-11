# Create your views here.
import simplejson as json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from movies.models import Movie, Genre, MovieContributors, Directory
from haystack.query import SearchQuerySet


def movie_dict(pk):
    movie = get_object_or_404(Movie, pk=pk)
    dic = {
        'title': movie.title,
        'title_fr': movie.title_fr,
        'title_int': movie.title_int,
        'year': movie.year,
        'runtime': movie.runtime,
        'id_imdb': movie.id_imdb,
        'poster': movie.poster,
        'rating': movie.rating,
        'votes': movie.votes,
        'plot': movie.plot,
        'language': movie.language,
        'directories': [(d.quality, d.location)
                  for d in Directory.objects.filter(movie=movie)]
    }
    return dic


def build_list(search_result):
    l = []
    for r in search_result:
        l.append(movie_dict(r.pk))
    return l


def details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    the_data = json.dumps({
        'results': {
            'title': movie.title,
            'title_int': movie.title_int,
            'title_fr': movie.title_fr,
            'id_imdb': movie.id_imdb
            }
        })
    return HttpResponse(the_data, content_type='application/json')


def search(request):
    sqs = SearchQuerySet().autocomplete(
            autocomplete=request.GET.get('q', ''))[:20]
    l = build_list(sqs)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': l
        })
    return HttpResponse(the_data, content_type='application/json')
