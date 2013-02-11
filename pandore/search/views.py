# Create your views here.
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
            autocomplete=request.GET.get('q', ''))[:5]
    for result in sqs:
        print result.title, result.score
    suggestions = [{
        'title': result.title,
        'url': '/movies/json/details/' + result.pk,
        } for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
        })
    return HttpResponse(the_data, content_type='application/json')
