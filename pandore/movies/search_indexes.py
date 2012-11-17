from haystack import indexes
from movies.models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    year = indexes.IntegerField(model_attr='year')

    def get_model(self):
        return Movie
