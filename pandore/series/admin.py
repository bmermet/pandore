from django.contrib import admin
from series.models import (Series, Season, Episode, Genre, SeriesContributors,
                           EpisodeContributors, SeriesDirectory,
                           SeasonDirectory, EpisodeDirectory)

c = (Series, Season, Episode, Genre, SeriesContributors, EpisodeContributors,
     SeriesDirectory, SeasonDirectory, EpisodeDirectory)
for m in c:
    admin.site.register(m)
