# Create your views here.
import simplejson as json
from django.http import HttpResponse
from movies.models import Movie, Genre, MovieContributors, Directory


def details(request, pk):
    if Movie.objects.filter(pk=pk).exists():
        movie = Movie.objects.get(pk=pk)
        the_data = json.dumps({
            'results': {
                'title': movie.title,
                'title_int': movie.title_int,
                'title_fr': movie.title_fr,
                'id_imdb': movie.id_imdb
                }
            })
    return HttpResponse(the_data, content_type='application/json')
