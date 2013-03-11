from haystack import indexes
from series.models import Episode, Series


class SeriesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    begin_year = indexes.IntegerField(model_attr='begin_year')
    end_year = indexes.IntegerField(model_attr='end_year')
    #autocomplete = indexes.EdgeNgramField(use_template=True)
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(SeriesIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Series


class EpisodeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    date = indexes.DateField(model_attr='date')
    runtime = indexes.IntegerField(model_attr='runtime')
    rating = indexes.FloatField(model_attr='rating')
    autocomplete = indexes.EdgeNgramField(use_template=True)
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(EpisodeIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Episode
