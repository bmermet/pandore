from django.contrib import admin
from movies.models import Movie, Genre, MovieContributors, Directory

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieContributors)
admin.site.register(Directory)
