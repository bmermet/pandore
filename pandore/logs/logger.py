from logs.models import Log


MOVIES = 0
SERIES = 1
MOVIES_UTILS = 2


class logger(object):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __init__(self, application_code):
        self.application_code = application_code

    def __request(self, level, error_code, message, pending):
        r = Log.objects.create(level=level,
                application_code=self.application_code, error_code=error_code,
                message=message, pending=pending)
        r.save()

    def debug(self, message, code=0, pending=False):
        self.__request(self.DEBUG, code, message, pending)

    def info(self, message, code=0, pending=False):
        self.__request(self.INFO, code, message, pending)

    def warning(self, message, code=0, pending=False):
        self.__request(self.WARNING, code, message, pending)

    def error(self, message, code=0, pending=False):
        self.__request(self.ERROR, code, message, pending)

    def critical(self, message, code=0, pending=False):
        self.__request(self.CRITICAL, code, message, pending)
