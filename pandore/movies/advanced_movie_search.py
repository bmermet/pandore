from django import forms
from haystack.forms import SearchForm


class AdvancedMovieSearchForm(SearchForm):
    begin_year = forms.IntegerField(required=False)
    end_year = forms.IntegerField(required=False)
    min_rating = forms.IntegerField(required=False)
    max_rating = forms.IntegerField(required=False)
    min_runtime = forms.IntegerField(required=False)
    max_runtime = forms.IntegerField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(AdvancedMovieSearchForm, self).search()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['begin_year']:
            sqs = sqs.filter(year__gte=self.cleaned_data['begin_year'])

        if self.cleaned_data['end_year']:
            sqs = sqs.filter(year__lte=self.cleaned_data['end_year'])

        if self.cleaned_data['min_rating']:
            sqs = sqs.filter(rating__gte=self.cleaned_data['min_rating'])

        if self.cleaned_data['max_rating']:
            sqs = sqs.filter(rating__lte=self.cleaned_data['max_rating'])

        if self.cleaned_data['min_runtime']:
            sqs = sqs.filter(runtime__gte=self.cleaned_data['min_runtime'])

        if self.cleaned_data['max_runtime']:
            sqs = sqs.filter(runtime__lte=self.cleaned_data['max_runtime'])

        return sqs
