from django.utils import timezone

from eliminationtournaments.models_interfaces import TournamentInterface
from .handler_interface import HandlerInterface


class StartMatchesHandler(HandlerInterface):

    def __init__(self, tournament: TournamentInterface) -> None:
        self.tournament = tournament

    def execute(self) -> None:
        now = timezone.now().timestamp()
        end_time = float(self.tournament.match_time) + now
        next_round = self.tournament.current_round + 1

        self.tournament.current_round = next_round
        self.tournament.match_ends = end_time
        self.tournament.save()
        
        end_date = timezone.datetime.fromtimestamp(end_time)
        print('==========================')
        print(end_date.strftime("%d/%m/%Y %H:%M:%S"))
        print('==========================')


        self.end_time = end_time


