from django.db import models
from people.models import Person


class Genre(models.Model):
    name = models.CharField(max_length=128)


class Series(models.Model):
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    nb_rates = models.IntegerField(verbose_name='number of rates')
    plot = models.TextField()
    language = models.CharField(max_length=2, verbose_name='main language')
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(
        Person, verbose_name='list of people involved',
        through='SeriesContributors')
    number_of_episodes = models.IntegerField(verbose_name='number of episodes')
    number_of_seasons = models.IntegerField(verbose_name='number of seasons')
    begin_year = models.IntegerField(verbose_name='begin year')
    end_year = models.IntegerField(verbose_name='end year')
    alias = models.CharField(max_length=16, verbose_name='series\' alias')

    def update_counts(self):
        c = 0
        for s in self.season_set.all():
            c += s.number_of_episodes
        self.number_of_episodes = c
        self.number_of_seasons = self.season_set.count()
        self.save()


class Season(models.Model):
    series = models.ForeignKey(Series)
    season_number = models.IntegerField(verbose_name='season number')
    number_of_episodes = models.IntegerField(verbose_name='number of episodes')

    def update_counts(self):
        self.number_of_episodes = self.episode_set.count()
        self.save()


class Episode(models.Model):
    season = models.ForeignKey(Season)
    episode_number = models.IntegerField(verbose_name='episode number')
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    nb_rates = models.IntegerField(verbose_name='number of rates')
    plot = models.TextField()
    date = models.DateField()
    runtime = models.IntegerField()
    persons = models.ManyToManyField(
        Person, verbose_name='list of people involved',
        through='EpisodeContributors')


class SeriesContributors(models.Model):
    person = models.ForeignKey(Person)
    series = models.ForeignKey(Series)
    function = models.CharField(max_length=1)


class EpisodeContributors(models.Model):
    person = models.ForeignKey(Person)
    episode = models.ForeignKey(Episode)
    function = models.CharField(max_length=1)


class SeriesDirectory(models.Model):
    series = models.ForeignKey(Series)
    location = models.CharField(max_length=256)


class SeasonDirectory(models.Model):
    season = models.ForeignKey(Season)
    location = models.CharField(max_length=256)
    quality = models.CharField(max_length=5)


class EpisodeDirectory(models.Model):
    episode = models.ForeignKey(Episode)
    location = models.CharField(max_length=256)
    quality = models.CharField(max_length=5)
    size = models.IntegerField(verbose_name='size in MB')
    addition_date = models.DateTimeField(
        auto_now_add=True, verbose_name='addition date')

