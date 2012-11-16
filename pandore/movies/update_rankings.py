from movies.models import Movie
from imdb import IMDb

i = IMDb()
for movie in Movie.objects.all():
    m = i.get_movie(movie.id_imdb)
    if not 'rating' in m.keys():
        continue
    movie.rating = m['rating']
    movie.votes = m['votes']
        movie.save()
