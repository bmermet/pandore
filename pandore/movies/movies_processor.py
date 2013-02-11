import guessit
import requests
import re
import os
from imdb import IMDb
from movies.models import Movie, Genre, MovieContributors, Directory
from people.models import Person
from utils.utils import get_size


__DEBUG__ = True


class DirectoryProcessor(object):
    __reg_dir_s = r'(.*/)?(.+)'
    __reg_bing_s = r'www.imdb.com/title/tt(?P<id>\d+)/'
    title = quality = year = id_imdb = None

    def __init__(self):
        self.__reg_dir = re.compile(self.__reg_dir_s)
        self.__reg_bing = re.compile(self.__reg_bing_s)
        self.reset_infos()
        self.movie = MovieProcessor()

    def reset_infos(self):
        self.title = self.quality = self.year = self.id_imdb = None
        self.directory = None
        self.processed = False

    def process(self, directory):
        self.reset_infos()
        self.directory = os.path.abspath(directory)
        existing = Directory.objects.filter(location=self.directory).exists()
        if existing:
            print 'Directory is already present in the database'
            return False
        dir = self.__reg_dir.match(self.directory).group(2) + '/'
        guess = guessit.guess_movie_info(dir.decode('utf-8'))
        if not ('title' and 'year') in guess:
            print 'Error while processing ' + self.directory
            return False
        search_string = 'site:imdb.com %s %s' % (
                guess['title'], str(guess['year']))
        r = requests.get(
                'http://www.bing.com/search', params={'q': search_string})
        match = self.__reg_bing.search(r.content)
        if not match:
            print r.url
            print "Bing wasn't able to find this movie, skipping"
            return False
        self.id_imdb = match.group('id')
        self.title = guess['title']
        self.year = guess['year']
        if 'screenSize' in guess:
            self.quality = guess['screenSize']
        else:
            self.quality = 'SD'
        #Size of the directory in Mo
        #TODO understand why the result is different from du
        self.size = (get_size(self.directory) + 500000) // 1000000
        self.save()
        return True

    def save(self):
        m = self.movie.process(self.id_imdb)
        Directory.objects.create(
                movie=m, location=self.directory,
                quality=self.quality, size=self.size)


class MovieProcessor(object):
    __reg_title_vf_s = r'(.+)::.*France'
    __reg_title_int_s = r'(.+)::.*International'
    __reg_runtime_s = r'\d+'
    title = title_fr = year = runtime = id_imdb = poster = rating = None
    votes = plot = language = genres = persons = None
    imdb_infos = None

    def __init__(self):
        self.__reg_title_vf = re.compile(self.__reg_title_vf_s)
        self.__reg_title_int = re.compile(self.__reg_title_int_s)
        self.__reg_runtime = re.compile(self.__reg_runtime_s)
        self.ia = IMDb()

    def reset_infos(self):
        self.title = self.title_fr = self.id_imdb = self.poster = ''
        self.plot = self.language = ''
        self.year = self.runtime = self.rating = self.votes = None
        self.genres = []
        self.persons = {'cast': [], 'director': [], 'writer': []}
        self.imdb_infos = None

    def get_title_fr(self):
        if 'akas' in self.imdb_infos.keys():
            for title in self.imdb_infos['akas']:
                match = self.__reg_title_vf.search(title)
                if match:
                    return match.group(1)
        return None

    def get_title_int(self):
        if 'akas' in self.imdb_infos.keys():
            for title in self.imdb_infos['akas']:
                match = self.__reg_title_int.search(title)
                if match:
                    return match.group(1)
        return None

    def process(self, id_imdb):
        self.reset_infos()
        self.id_imdb = id_imdb
        existing = Movie.objects.filter(id_imdb=id_imdb).exists()
        if existing:
            print "Movie already in the database"
            return Movie.objects.get(id_imdb=id_imdb)
        self.imdb_infos = self.ia.get_movie(id_imdb)
        if not len(self.imdb_infos):
            print 'Unvalid imdb id : %s, aborting...' % id_imdb
            return False
        self.title = self.imdb_infos['title']
        self.year = self.imdb_infos['year']
        self.title_fr = self.get_title_fr()
        if self.title_fr:
            self.title_fr = self.title_fr.encode('utf-8')
        else:
            self.title_fr = self.title
        self.title_int = self.get_title_int()
        if self.title_int:
            self.title_int = self.title_int.encode('utf-8')
        else:
            self.title_int = self.title
        if 'runtimes' in self.imdb_infos.keys():
            match = self.__reg_runtime.search(self.imdb_infos['runtimes'][0])
            if match:
                self.runtime = match.group(0)
        if 'cover url' in self.imdb_infos.keys():
            self.poster = self.imdb_infos['cover url']
        if 'rating' in self.imdb_infos.keys():
            self.rating = self.imdb_infos['rating']
        if 'votes' in self.imdb_infos.keys():
            self.votes = self.imdb_infos['votes']
        if 'plot outline' in self.imdb_infos.keys():
            self.plot = self.imdb_infos['plot outline']
        if 'language codes' in self.imdb_infos.keys():
            self.language = self.imdb_infos['language codes'][0]
        if 'genres' in self.imdb_infos.keys():
            self.genres = self.imdb_infos['genres']
        if 'cast' in self.imdb_infos.keys():
            self.persons['cast'] = self.imdb_infos['cast']
        if 'director' in self.imdb_infos.keys():
            self.persons['director'] = self.imdb_infos['director']
        if 'writer' in self.imdb_infos.keys():
            self.persons['writer'] = self.imdb_infos['writer']
        #TODO take care of encoding where it needs to.
        m = self.save()
        return m

    def save(self):
        if __DEBUG__:
            print "title : " + self.title
            print "title_fr : " + self.title_fr
            print "title_int : " + self.title_int
            print "year : " + str(self.year)
            if self.runtime:
                print "runtime : " + self.runtime
            print "poster : " + self.poster
            if self.rating:
                print "rating : " + str(self.rating)
            if self.votes:
                print "votes : " + str(self.votes)
            print "plot : " + self.plot
            print "language : " + self.language
        m = Movie.objects.create(
                title=self.title, title_fr=self.title_fr,
                title_int=self.title_int, year=self.year,
                runtime=self.runtime, id_imdb=self.id_imdb,
                poster=self.poster, rating=self.rating,
                votes=self.votes, plot=self.plot,
                language=self.language)
        m.save()
        for idx, actor in enumerate(self.persons['cast']):
            p = Person.add(actor)
            MovieContributors.objects.create(
                    person=p, movie=m, function='A', rank=idx)
        for idx, director in enumerate(self.persons['director']):
            p = Person.add(director)
            MovieContributors.objects.create(
                    person=p, movie=m, function='D', rank=idx)
        for idx, writer in enumerate(self.persons['writer']):
            p = Person.add(writer)
            p.save()
            MovieContributors.objects.create(
                    person=p, movie=m, function='W', rank=idx)
        for genre in self.genres:
            g = Genre.add(genre)
            m.genres.add(g)
        return m
