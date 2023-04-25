from eliminationtournaments.outer_layer.repositories import TournamentRepository
from eliminationtournaments.inner_layer.entities import TournamentEntity


class CreateTournamentUseCase:

    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    def execute(self, tournament: TournamentEntity) -> TournamentEntity:
        if tournament.tournament_type == 'elimination':
            tournament.current_round = 1
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
