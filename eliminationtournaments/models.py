from django.db import models

from .inner_layer.entities import (TournamentEntity, RoundEntity, PlayerEntity, 
    PositionEntity, MatchEntity)
# Create your models here.

class Tournament(models.Model):
    name: str = models.CharField(default='unamed tournament', max_length=80)
    size = models.IntegerField(default=8)
    tournament_type = models.CharField(max_length=80)
    # started, ended, created, draft
    status = models.CharField(default='draft',  max_length=20)
    current_round = models.IntegerField(default=0)
    total_rounds = models.IntegerField
    match_time = models.IntegerField
    # positions = models.ManyToOneRel
    # players = models.ManyToOneRel
    # rounds = models.ManyToOneRel

    @staticmethod
    def from_entity(entity: TournamentEntity) -> 'Tournament':
        return Tournament(
            id=entity.id,
            name=entity.name,
            size=entity.size,
            tournament_type=entity.tournament_type,
            status=entity.status,
            current_round=entity.current_round,
            total_rounds=entity.total_rounds,
            match_time=entity.match_time,
            # Player.objects.filter(id__in=player_ids)
            positions_ids=entity.positions,
            players_ids=entity.players,  # Player.objects.filter(id__in=player_ids)
            rounds_ids=entity.rounds  # Player.objects.filter(id__in=player_ids)
        )

    def to_entity(self) -> TournamentEntity:
        return TournamentEntity(
            int(self.id),
            self.name,
            self.size,
            self.tournament_type,
            self.status,
            self.current_round,
            self.total_rounds,
            self.match_time,
            self.positions.values_list('id', flat=True),
            self.players.values_list('id', flat=True),
            self.rounds.values_list('id', flat=True),
        )


class Round(models.Model):
    round_number = models.IntegerField
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    # matches = models.ManyToOneRel

    @staticmethod
    def from_entity(entity: RoundEntity) -> 'Round':
        return Round(
            round_number= entity.round_number,
            tournament_id= entity.tournament_id,
            matches_ids= entity.matches_ids
        )

    def to_entity(self) -> RoundEntity:
        return RoundEntity(
            self.id,
            self.round_number,
            self.tournament.id,
            matches_ids= self.matches.values_list('id', flat=True)
        )

class Player(models.Model):
    avatar = models.CharField(max_length=255)
    name = models.CharField(max_length=60)

    @staticmethod
    def from_entity(entity: PlayerEntity) -> 'Player':
        return Player(id= entity.id, avatar= entity.avatar, name= entity.name)

    def to_entity(self) -> RoundEntity:
        return RoundEntity(self.id, self.avatar, self.name)

class Position(models.Model):
    order = models.IntegerField
    votes = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    next_position = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL)

    @staticmethod
    def from_entity(entity: PositionEntity) -> 'Position':
        return Position(
            id= entity.id,
            order= entity.order,
            votes= entity.votes,
            tournament_id= entity.tournament,
            player_id= entity.player,
            next_position= entity.next_position,
        )

    def to_entity(self) -> PositionEntity:
        return PositionEntity(
            self.id,
            self.order,
            self.votes,
            self.tournament.id,
            self.player.id,
            self.next_position.id
        )

class Match(models.Model):
    position_one = models.ForeignKey(
        Position, null=True, blank=True, on_delete=models.SET_NULL)
    position_two = models.ForeignKey(
        Position, null=True, blank=True, on_delete=models.SET_NULL)
    disabled = models.BooleanField
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    @staticmethod
    def from_entity(entity: MatchEntity) -> 'Match':
        return Match(
            position_one=entity.position_one,
            position_two=entity.position_two,
            disabled=entity.disabled,
            round_id=entity.round_id,
        )

    def to_entity(self) -> MatchEntity:
        return MatchEntity(
            self.position_one.id,
            self.position_two.id,
            self.disabled,
            self.round.id,
        )
