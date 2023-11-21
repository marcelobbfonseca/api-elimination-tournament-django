from django.apps import apps
from django.db import models

class TournamentInterface(models.Model):
    
    class Meta:
        abstract = True
    
    def get_tournament():
        Tournament = apps.get_model('eliminationtournaments', 'Tournament')
        return Tournament

class PositionInterface(models.Model):

    class Meta:
        abstract = True

    def get_position():
        Position = apps.get_model('eliminationtournaments', 'Position')
        return Position

class PlayerInterface(models.Model):

    class Meta:
        abstract = True
