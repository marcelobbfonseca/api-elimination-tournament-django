from ..models import Tournament, Round
from ..inner_layer.entities import TournamentEntity, RoundEntity


class TournamentRepository:

    def save(self, entity: TournamentEntity) -> Tournament:
        model = Tournament.from_entity(entity)
        model.save()
        model.to_entity()


class RoundRepository:

    def matches(self, entity: RoundEntity):
        model = Round.from_entity(entity)
        return list(model.matches.values())
