from django.db import models
from people.models import Person


class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True)

    @classmethod
    def add(cls, genre):
        g = Genre.objects.filter(name=genre)
        if len(g):
            return g[0]
        return Genre.objects.create(name=genre)

    def __unicode__(self):
        return 'name : ' + self.name


class Movie(models.Model):
    PROFESSION_CODE = (
            ('A', 'Actor'),
            ('D', 'Director'),
            ('W', 'Writer'),
            )
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    title_int = models.CharField(max_length=256,
            verbose_name='international title')
    year = models.IntegerField()
    runtime = models.IntegerField()
    id_imdb = models.CharField(
            max_length=7, unique=True, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    votes = models.IntegerField(verbose_name='number of votes')
    plot = models.TextField()
    language = models.CharField(max_length=2, verbose_name='main language')
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person,
            verbose_name='list of people involved',
            through='MovieContributors')

    def __unicode__(self):
        return 'title : ' + self.title + '; id_imdb : ' + self.id_imdb


class MovieContributors(models.Model):
    person = models.ForeignKey(Person)
    movie = models.ForeignKey(Movie)
    function = models.CharField(max_length=1)
    rank = models.IntegerField()

    def __unicode__(self):
        return 'person : ' + self.person.name + '; movie : ' + self.movie.title


class Directory(models.Model):
    movie = models.ForeignKey(Movie)
    location = models.CharField(max_length=256, unique=True)
    quality = models.CharField(max_length=5)
    size = models.IntegerField(verbose_name='size in MB')
    addition_date = models.DateTimeField(auto_now_add=True,
            verbose_name='addition date')

    def __unicode__(self):
        return 'movie : ' + self.movie.title + 'location : ' + self.location
