
from .handler_interface import HandlerInterface
from eliminationtournaments.models_interfaces import TournamentInterface
from eliminationtournaments.use_cases.create_brackets import create_elimination_tournament_brackets_usecase

class CreateBracketsHandler(HandlerInterface):


    def __init__(self, tournament: TournamentInterface) -> None:
        self.tournament = tournament

    def execute(self) -> None:
        if self.tournament.tournament_type == 'elimination':
            self.tournament.set_total_rounds_by_size()
            self.tournament.save()
            create_elimination_tournament_brackets_usecase(self.tournament)