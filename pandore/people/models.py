from django.db import models


class Person(models.Model):
    id_imdb = models.CharField(
            max_length=7, unique=True, verbose_name='imdb id')
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return 'id_imdb: ' + self.id_imdb + '; name: ' + self.name

    def add(person):
        p = Person.objects.filter(id_imdb=person.personID)
        if len(p):
            return p[0]
        p = Person(id_imdb=person.personID, name=person['name'])
        p.save()
        return p
