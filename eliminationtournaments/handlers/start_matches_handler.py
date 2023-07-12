from datetime import datetime
import schedule
from eliminationtournaments.models_interfaces import TournamentInterface
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from .handler_interface import HandlerInterface

class StartMatchesHandler(HandlerInterface):

    def __init__(self, tournament: TournamentInterface) -> None:
        self.tournament = tournament

    def execute(self) -> None:
        now = datetime.now().timestamp()
        end_time = self.tournament.match_time + now
        next_round = self.tournament.current_round + 1
        self.tournament.set_current_round(next_round)
        self.tournament.set_match_end_time(end_time)
        self.tournament.save()

        end_date = datetime.fromtimestamp(end_time)
        schedule.every().day.at(end_date.strftime('%H:%M:%S')).do(self.call_end_match(self.tournament))

    def call_end_match(self):
        print('alooo')
        end_matches = EndMatchesHandler(self)
        end_matches.execute()
        return schedule.CancelJob

# import time

# def job_that_executes_once():
#     # Do some work that only needs to happen once...
#     return schedule.CancelJob

# schedule.every().day.at('22:30').do(job_that_executes_once)

# while True:
#     schedule.run_pending()
#     time.sleep(1)