from django.utils import timezone
# import schedule
# from eliminationtournaments.singletons import BGScheduler

from eliminationtournaments.models_interfaces import TournamentInterface
from .handler_interface import HandlerInterface
from tournament_api.settings import TIME_ZONE
from eliminationtournaments.tasks import end_match


class StartMatchesHandler(HandlerInterface):

    def __init__(self, tournament: TournamentInterface) -> None:
        self.tournament = tournament

    def execute(self) -> None:
        now = timezone.now().timestamp()
        end_time = float(self.tournament.match_time) + now
        next_round = self.tournament.current_round + 1

        self.tournament.set_current_round(next_round)
        self.tournament.set_match_end_time(end_time)
        self.tournament.save()
        
        end_date = timezone.datetime.fromtimestamp(end_time)
        print('==========================')
        print(end_date.strftime("%d/%m/%Y %H:%M:%S"))
        print('==========================')

        end_match.apply_async(
            args=[self.tournament.id],
            eta=end_time,
        )
