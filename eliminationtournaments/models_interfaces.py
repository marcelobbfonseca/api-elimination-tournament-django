from django.apps import apps
from django.db import models
from abc import ABC

class TournamentStatuses(ABC):
    ALL = ('started', 'ended', 'created', 'draft')
    STARTED='started'
    ENDED='ended'
    CREATED='created'
    DRAFT='draft'

class TournamentInterface(models.Model):
    id: int
    name: str
    size: int
    tournament_type: str
    status: str
    current_round: int
    total_rounds: int
    match_time: int
    match_ends: float
    views: int
    
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
