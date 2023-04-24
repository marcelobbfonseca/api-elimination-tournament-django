from eliminationtournaments.models import Tournament, Round, Match, Player, Position
from eliminationtournaments.inner_layer.entities import TournamentEntity, RoundEntity, MatchEntity, PlayerEntity, PositionEntity


class TournamentRepository:

    def save(self, entity: TournamentEntity) -> Tournament:
        model = Tournament.from_entity(entity)
        model.save()
        return model.to_entity()


class RoundRepository:

    def save(self, entity: RoundEntity) -> Round:
        model = Round.from_entity(entity)
        model.save()
        return model.to_entity()

    def matches(self, entity: RoundEntity):
        model = Round.from_entity(entity)
        return list(model.matches.values())

class MatchRepository:
    def save(self, entity: MatchEntity) -> Match:
        model = Match.from_entity(entity)
        model.save()
        return model.to_entity()
        
class PlayerRepository:
    def save(self, entity: PlayerEntity) -> Player:
        model = Player.from_entity(entity)
        model.save()
        return model.to_entity()

class PositionRepository:
    def save(self, entity: PositionEntity) -> Position:
        model = Position.from_entity(entity)
        model.save()
        return model.to_entity()
