from django.db import models


class Person(models.Model):
    id_imdb = models.CharField(max_length=7, verbose_name='imdb id')
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return 'id_imdb: ' + self.id_imdb + '; name: ' + self.name
