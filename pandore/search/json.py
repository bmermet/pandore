import simplejson as json
from series.models import Episode, Series
from movies.models import Movie
from haystack.query import SearchQuerySet
from django.http import HttpResponse
from series.json import episode_dict, series_dict
from movies.json import movie_dict


def build_list(search_result):
    s = []
    e = []
    m = []
    for r in search_result:
        if r.content_type() == 'series.episode':
            e.append(episode_dict(r.pk))
        if r.content_type() == 'series.series':
            s.append(series_dict(r.pk))
        if r.content_type() == 'movies.movie':
            m.append(movie_dict(r.pk))
    return {"series": s, "episodes": e, "movies": m}


def search(request):
    t = request.GET.get('t', 'any')
    if t == 'movies':
        models_type = [Movie]
    elif t == 'series':
        models_type = [Series, Episode]
    else:
        models_type = [Series, Episode, Movie]
    sqs = SearchQuerySet().models(*models_type).autocomplete(
        text=request.GET.get('q', ''))
    l = build_list(sqs)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': l
        })
    return HttpResponse(the_data, content_type='application/json')
