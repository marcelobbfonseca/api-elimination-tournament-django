from django.test import TestCase
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler
from eliminationtournaments.models import Tournament, Position, Player


class MatchHandlerTest(TestCase):

    def test_end_matchs_handler(self):
        tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=2,
            tournament_type='elimination',
            status='started',
            current_round=1,
            total_rounds=1,
            match_time=10
        )
        loser = Player.objects.create(avatar='C://path/my_img.jpg', name='Bowser')
        winner = Player.objects.create(avatar='C://path/my_img.jpg', name='Shy guy')
        position = Position.objects.create(
            depth=0,
            votes=0,
            tournament=tournament
        )
        position.right_position = Position.objects.create(
            depth=1,
            votes=1,
            tournament=tournament,
            player=loser
        )
        position.left_position = Position.objects.create(
            depth=1,
            votes=3,
            tournament=tournament,
            player=winner
        )
        position.save()
        start_match = StartMatchesHandler(tournament)
        end_match_handler = EndMatchesHandler(start_match)
        end_match_handler.execute()
        position.refresh_from_db()
        self.assertEqual(winner, position.player)
