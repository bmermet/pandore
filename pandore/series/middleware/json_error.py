# Middleware to catch JSON errors from our views,

from django.http import HttpResponseNotFound
import simplejson as json


class JsonException(Exception):
    pass


class JsonExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, JsonException):
            return None

        return HttpResponseNotFound(json.dumps({
            'results': []}), content_type='application/json')
