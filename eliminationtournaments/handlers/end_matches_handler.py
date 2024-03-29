
from eliminationtournaments.models_interfaces import PositionInterface as Position
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.use_cases.position_usecases import calculate_winner_usecase
from eliminationtournaments.handlers.handler_interface import HandlerInterface

class EndMatchesHandler():

    def __init__(self, start_match: HandlerInterface) -> None:
        self.tournament = start_match.tournament
        self.start_match = start_match

    def execute(self) -> None:
        winning_positions = Position.get_position().objects.filter(
            tournament__id=self.tournament.id,
            player=None
        ).exclude(
            left_position__player__isnull=True,
            right_position__player__isnull=True
        )
        for position in winning_positions:
            winner = calculate_winner_usecase(position)
            position.set_player(winner)
            position.save()
        print("current_round: {} total_rounds: {}".format(self.tournament.current_round, self.tournament.total_rounds))
        if self.tournament.current_round == self.tournament.total_rounds:
            self.tournament.set_tournament_status(TournamentStatuses.ENDED)
            self.tournament.save()
            print('Tournament end')
        else:
            self.start_match.execute()
