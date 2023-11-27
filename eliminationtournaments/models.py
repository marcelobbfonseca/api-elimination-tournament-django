from django.db import models
from .models_interfaces import TournamentInterface, PositionInterface
from eliminationtournaments.inner_layer.entities import (TournamentEntity, RoundEntity, PlayerEntity, 
    PositionEntity, MatchEntity, DEFAULT_MATCH_TIME)

from eliminationtournaments.signals import start_tournament, create_brackets




class Tournament(TournamentInterface):
    name = models.CharField(default='unamed tournament', max_length=80)
    size = models.IntegerField(default=8)
    tournament_type = models.CharField(max_length=80, default='elimination')
    status = models.CharField(default='draft',  max_length=20)# started, ended, created, draft
    current_round = models.IntegerField(default=0)
    total_rounds = models.IntegerField(default=0)
    match_time = models.IntegerField(default=DEFAULT_MATCH_TIME)
    match_ends = models.FloatField(default=0.0)
    # positions = models.ManyToOneRel positions_set.add() .all() .count() .filter
    # players = models.ManyToOneRel
    # rounds = models.ManyToOneRel
    def set_current_round(self, round: int):
        self.current_round = round

    def set_match_end_time(self, time: int):
        self.match_ends = time

    def set_tournament_status(self, status: str):
        self.status = status

    def set_total_rounds_by_size(self) -> None:
        if self.size == 8:
            self.total_rounds = 3
        elif self.size == 4:
            self.total_rounds = 2
        elif self.size == 2:
            self.total_rounds == 1


    def get_champion(self):
        return self.position_set.get(depth=0)

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
            # positions_ids=entity.positions,
            # players_ids=entity.players,  # Player.objects.filter(id__in=player_ids)
            # rounds_ids=entity.rounds  # Player.objects.filter(id__in=player_ids)
        )

    def to_entity(self) -> TournamentEntity:
        return TournamentEntity(
            self.name,
            self.size,
            self.tournament_type,
            id=int(self.id),
            status=self.status,
            current_round=self.current_round,
            total_rounds=self.total_rounds,
            match_time=self.match_time,
            # self.positions.values_list('id', flat=True),
            # self.players.values_list('id', flat=True),
            # self.rounds.values_list('id', flat=True),
        )

    def __repr__(self) -> str:
        return "<{},{}>".format(self.id, self.name)

    def __str__(self) -> str:
        return "<{},{}>".format(self.id, self.name)


class Player(models.Model):
    avatar = models.CharField(max_length=255)
    name = models.CharField(max_length=60)

    @staticmethod
    def from_entity(entity: PlayerEntity) -> 'Player':
        return Player(id= entity.id, avatar= entity.avatar, name= entity.name)

    def to_entity(self) -> RoundEntity:
        return RoundEntity(self.id, self.avatar, self.name)

    def __repr__(self) -> str:
        return "<{},{}>".format(self.id, self.name)

    def __str__(self) -> str:
        return "<{},{}>".format(self.id, self.name)


class Position(PositionInterface):
    depth = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL)
    bracket_index  = models.IntegerField(default=-1)
    # left tree node
    left_position = models.OneToOneField(
        'self', null=True, blank=True,related_name='next_left', on_delete=models.SET_NULL)
    # right tree node
    right_position =models.OneToOneField(
        'self', default=None, null=True, blank=True,related_name='next_right', on_delete=models.SET_NULL)     

    def next_position(self):
        left = self.get_next_left()
        if left is not None:
            return left
        right = self.get_next_right()
        if right is not None:
            return right
        return None
    def get_next_right(self):
        try:
            return self.next_right
        except self.DoesNotExist:
            return None
    def get_next_left(self):
        try:
            return self.next_left
        except self.DoesNotExist:
            return None

    def set_player(self, player: Player) -> None:
        self.player = player
    
    def increment_vote(self) -> None:
        self.votes+=1

    @staticmethod
    def from_entity(entity: PositionEntity) -> 'Position':
        return Position(
            id= entity.id,
            depth= entity.order,
            votes= entity.votes,
            tournament_id= entity.tournament,
            player_id= entity.player,
        )

    def to_entity(self) -> PositionEntity:
        return PositionEntity(
            self.id,
            self.depth,
            self.votes,
            self.tournament.id,
            self.player.id,
            self.next_position.id
        )


    def __str__(self) -> str:
        player = self.player.name if self.player is not None else None
        left = self.left_position.id if self.left_position is not None else None
        right = self.right_position.id if self.right_position is not None else None
        next =  self.next_position().id if self.next_position() is not None else None
        return "<{},{}, depth: {}, {}, left: {},next: {}, right: {}>".format(self.id, self.tournament.name, self.depth, player, left, next, right)



models.signals.post_save.connect(start_tournament, sender=Tournament)
# models.signals.post_save.connect(create_brackets, sender=Tournament)