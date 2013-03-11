import simplejson as json
from series.models import (Episode, Series, Season,
                           EpisodeDirectory, SeriesDirectory)
from django.shortcuts import get_object_or_404 as orig_get_object_or_404
from django.shortcuts import render
from haystack.query import SearchQuerySet
from django.http import HttpResponse, Http404
from series.middleware.json_error import JsonException


def get_object_or_404(klass, *args, **kwargs):
    try:
        return orig_get_object_or_404(klass, *args, **kwargs)
    except Http404:
        raise JsonException()


def episode_dict(pk):
    episode = get_object_or_404(Episode, pk=pk)
    dic = {
        'series_title': episode.season.series.title,
        'series_title_fr': episode.season.series.title_fr,
        'series_title_int': episode.season.series.title_int,
        'series_id_imdb': episode.season.series.id_imdb,
        'episode_number': episode.episode_number,
        'season_number': episode.season.season_number,
        'title': episode.title,
        'title_fr': episode.title_fr,
        'date': episode.date.strftime("%d/%m/%Y"),
        'runtime': episode.runtime,
        'id_imdb': episode.id_imdb,
        'poster': episode.poster,
        'rating': episode.rating,
        'votes': episode.votes,
        'plot': episode.plot,
        'directories': [(d.quality, d.location)
                  for d in EpisodeDirectory.objects.filter(episode=episode)]
    }
    return dic


def series_dict(pk):
    series = get_object_or_404(Series, pk=pk)
    dic = {
        'title': series.title,
        'title_fr': series.title_fr,
        'title_int': series.title_int,
        'id_imdb': series.id_imdb,
        'begin_year': series.begin_year,
        'end_year': series.end_year,
        'poster': series.poster,
        'rating': series.rating,
        'votes': series.votes,
        'plot': series.plot,
        'language': series.language,
        'directory': SeriesDirectory.objects.get(series=series).location,
        'seasons': [(s.season_number, Episode.objects.filter(season=s).count())
                    for s in Season.objects.filter(series=series)]
    }
    dic['seasons'] = sorted(dic['seasons'], key=lambda s: s[0])
    return dic


def build_list(search_result):
    s = []
    e = []
    for r in search_result:
        if r.content_type() == 'series.episode':
            e.append(episode_dict(r.pk))
        if r.content_type() == 'series.series':
            s.append(series_dict(r.pk))
    return {"series": s, "episodes": e}


def details_series(request, id_imdb):
    s = get_object_or_404(Series, id_imdb=id_imdb)
    the_data = json.dumps({
        'results': series_dict(s.pk)
        })
    return HttpResponse(the_data, content_type='application/json')


def details_episode(request, series_id_imdb, season_number, episode_number):
    s = get_object_or_404(Series, id_imdb=series_id_imdb)
    e = get_object_or_404(
        Episode, season__series=s, season__season_number=season_number, episode_number=episode_number)
    the_data = json.dumps({
        'results': episode_dict(e.pk)
        })
    return HttpResponse(the_data, content_type='application/json')


def details_season(request, series_id_imdb, season_number):
    series = get_object_or_404(Series, id_imdb=series_id_imdb)
    episodes = Episode.objects.filter(
        season__series=series, season__season_number=season_number)
    the_data = json.dumps({
        'results': [episode_dict(ep.pk) for ep in episodes]
        })
    return HttpResponse(the_data, content_type='application/json')


def details(request, pk):
    s = get_object_or_404(Series, pk=pk)
    context = {'object': s}
    return render(request, 'series/test2.html', context)


def search(request):
    sqs = SearchQuerySet().models(Series, Episode).autocomplete(
        text=request.GET.get('q', ''))[:30]
    l = build_list(sqs)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': l
        })
    return HttpResponse(the_data, content_type='application/json')
