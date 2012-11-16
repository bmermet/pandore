from haystack import indexes
from movies.models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titre = indexes.CharField(model_attr='title')
    annee = indexes.IntegerField(model_attr='year')

    def get_model(self):
        return Movie
