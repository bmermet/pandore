from haystack import indexes
from movies.models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    year = indexes.IntegerField(model_attr='year')
    runtime = indexes.IntegerField(model_attr='runtime')
    rating = indexes.FloatField(model_attr='rating')
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(MovieIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Movie
