from django.db import models
from people.models import Person


class Genre(models.Model):
    name = models.CharField(max_length=128)


class Movie(models.Model):
    PROFESSION_CODE = (
            ('A', 'Actor'),
            ('D', 'Director'),
            ('W', 'Writer'),
            )
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    year = models.IntegerField()
    runtime = models.IntegerField()
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    nb_rates = models.IntegerField(verbose_name='number of rates')
    plot = models.TextField()
    language = models.CharField(max_length=2, verbose_name='main language')
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person,
            verbose_name='list of people involved',
            through='MovieContributors')


class MovieContributors(models.Model):
    person = models.ForeignKey(Person)
    movie = models.ForeignKey(Movie)
    function = models.CharField(max_length=1)


class Directory(models.Model):
    movie = models.ForeignKey(Movie)
    location = models.CharField(max_length=256)
    quality = models.CharField(max_length=5)
    size = models.IntegerField(verbose_name='size in MB')
    addition_date = models.DateTimeField(auto_now_add=True,
            verbose_name='addition date')
