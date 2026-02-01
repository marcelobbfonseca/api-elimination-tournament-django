
from eliminationtournaments.models_interfaces import PositionInterface as Position, TournamentInterface
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.use_cases.position_usecases import calculate_winner_usecase
from eliminationtournaments.handlers.handler_interface import HandlerInterface

class EndMatchesHandler():

    def __init__(self, tournament: TournamentInterface) -> None:
        self.tournament = tournament

    def execute(self) -> None:

        """
        Ends the current match round:
        - Calculates winners
        - Advances positions
        - Updates tournament state
        """

        # Idempotency guard
        if self.tournament.status == TournamentStatuses.ENDED:
            return


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
        
        # Decide next step (pure state decision)
        if self.tournament.current_round >= self.tournament.total_rounds:
            self.tournament.set_tournament_status(TournamentStatuses.ENDED)
            self.tournament.save()
            print('Tournament end')
        else:
            # Advance round only, no scheduling here
            self.tournament.set_current_round(self.tournament.current_round + 1)
            self.tournament.save()
