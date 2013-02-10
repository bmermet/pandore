from django.db import models
import datetime
from django.utils.timezone import utc


# Create your models here.
class Log(models.Model):
    LOG_LEVEL = (
            (0, 'DEBUG'),
            (1, 'INFO'),
            (2, 'WARNING'),
            (3, 'ERROR'),
            (4, 'CRITICAL'),
            )
    level = models.IntegerField(choices=LOG_LEVEL)
    application_code = models.IntegerField(null=True)
    error_code = models.IntegerField(null=True)
    message = models.TextField()
    pending = models.NullBooleanField()
    date = models.DateTimeField(
            default=datetime.datetime.utcnow().replace(tzinfo=utc))

    def __unicode__(self):
        return (self.get_level_display() + ' ' + str(self.error_code) + ' ' +
                self.message + (self.pending and ' PENDING' or ''))
