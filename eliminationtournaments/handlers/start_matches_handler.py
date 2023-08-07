from django.utils import timezone
# import schedule
from eliminationtournaments.singletons import BGScheduler
from eliminationtournaments.models_interfaces import TournamentInterface
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from .handler_interface import HandlerInterface
from tournament_api.settings import TIME_ZONE
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

        bg = BGScheduler.get_instance()
        bg.sched.add_job(self.call_end_match, 'date', run_date=end_date, timezone=TIME_ZONE)

    def call_end_match(self):
        print('start job')
        end_matches = EndMatchesHandler(self)
        end_matches.execute()
