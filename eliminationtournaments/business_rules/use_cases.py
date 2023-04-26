from eliminationtournaments.outer_layer.repositories import TournamentRepository
from eliminationtournaments.inner_layer.entities import TournamentEntity
from typing import List


class CreateTournamentUseCase:

    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self, tournament: TournamentEntity) -> TournamentEntity:
        if tournament.tournament_type == 'elimination':
            tournament.current_round = 0
            if tournament.size == 4:
                tournament.total_rounds = 2
            if tournament.size == 8:
                tournament.total_rounds = 3
            if tournament.size == 16:
                tournament.total_rounds = 4
        return self.repository.save(tournament)


class FindTournamentUseCase:

    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self, id: int) -> TournamentEntity | None:
        return self.repository.find(id)


class ListTournamentsUseCase:
    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self) -> List[TournamentEntity]:
        return self.repository.all()


class DeleteTournamentUseCase:

    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self, id: int) -> TournamentEntity | None:
        return self.repository.delete(id)


class UpdateTournamentUseCase:

    PERMITTED_PARAMS = ['name', 'size', 'tournament_type', 'status', 'match_time']

    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self, tournament: TournamentEntity, params: TournamentEntity) -> TournamentEntity | None:
        for key in self.PERMITTED_PARAMS:
            tournament[key] = params[key] if params[key] is not None else False
        return self.repository.save(tournament)

