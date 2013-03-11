from django.db import models
from people.models import Person


class Genre(models.Model):
    name = models.CharField(max_length=128)

    @classmethod
    def add(cls, genre):
        g = Genre.objects.filter(name=genre)
        if len(g):
            return g[0]
        return Genre.objects.create(name=genre)

    def __unicode__(self):
        return 'Name : ' + self.name


class Series(models.Model):
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    title_int = models.CharField(max_length=256,
            verbose_name='international title')
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    votes = models.IntegerField(verbose_name='number of votes')
    plot = models.TextField()
    language = models.CharField(max_length=3, verbose_name='main language')
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

    def __unicode__(self):
        return 'Title : ' + self.title_int + '; Id_imdb : ' + self.id_imdb


class Season(models.Model):
    series = models.ForeignKey(Series)
    season_number = models.IntegerField(verbose_name='season number')
    number_of_episodes = models.IntegerField(verbose_name='number of episodes')

    def update_counts(self):
        self.number_of_episodes = self.episode_set.count()
        self.save()

    def __unicode__(self):
        return '%s S%d'%(self.series.title, self.season_number)


class Episode(models.Model):
    season = models.ForeignKey(Season)
    episode_number = models.IntegerField(verbose_name='episode number')
    title = models.CharField(max_length=256, verbose_name='original title')
    title_fr = models.CharField(max_length=256, verbose_name='french title')
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    poster = models.CharField(max_length=256, verbose_name='poster url')
    rating = models.FloatField()
    votes = models.IntegerField(verbose_name='number of votes')
    plot = models.TextField()
    date = models.DateField()
    runtime = models.IntegerField()
    persons = models.ManyToManyField(
        Person, verbose_name='list of people involved',
        through='EpisodeContributors')

    def __unicode__(self):
        return '%s S%dE%d'%(
                self.season.series.title, self.season.season_number,
                self.episode_number)


class SeriesContributors(models.Model):
    PROFESSION_CODE = (
            ('A', 'Actor'),
            ('D', 'Director'),
            ('W', 'Writer'),
            )
    person = models.ForeignKey(Person)
    series = models.ForeignKey(Series)
    function = models.CharField(max_length=1, choices=PROFESSION_CODE)
    rank = models.IntegerField(null=True)

    def __unicode__(self):
        return 'Person : ' + self.person.name + '; Series : ' + self.series.title


class EpisodeContributors(models.Model):
    PROFESSION_CODE = (
            ('A', 'Actor'),
            ('D', 'Director'),
            ('W', 'Writer'),
            )
    person = models.ForeignKey(Person)
    episode = models.ForeignKey(Episode)
    function = models.CharField(max_length=1, choices=PROFESSION_CODE)
    rank = models.IntegerField(null=True)

    def __unicode__(self):
        return 'Person: %s - %s S%dE%d' % (
                self.person.name, self.episode.season.series.title,
                self.episode.season.season_number, self.episode.episode_number)


class SeriesDirectory(models.Model):
    series = models.ForeignKey(Series)
    location = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return 'Location: ' + self.location


class SeasonDirectory(models.Model):
    season = models.ForeignKey(Season)
    location = models.CharField(max_length=255, unique=True)
    quality = models.CharField(max_length=5)

    def __unicode__(self):
        return 'Location: ' + self.location


class EpisodeDirectory(models.Model):
    episode = models.ForeignKey(Episode)
    location = models.CharField(max_length=255, unique=True)
    quality = models.CharField(max_length=5)
    size = models.IntegerField(verbose_name='size in MB')
    addition_date = models.DateTimeField(
        auto_now_add=True, verbose_name='addition date')

    def __unicode__(self):
        return 'Location: ' + self.location

