from django.apps import apps
from django.db import models

class TournamentInterface(models.Model):
    
    class Meta:
        abstract = True

class PositionInterface(models.Model):

    class Meta:
        abstract = True

    # @abstractmethod
    def get_position():
        Position = apps.get_model('eliminationtournaments', 'Position')
        return Position

class PlayerInterface(models.Model):

    class Meta:
        abstract = True
