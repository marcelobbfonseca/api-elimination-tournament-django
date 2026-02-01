from django.test import TestCase
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler
from eliminationtournaments.handlers.create_brackets_handler import CreateBracketsHandler
from eliminationtournaments.models import Tournament, Position, Player
from eliminationtournaments.use_cases.create_brackets import SIZE_8_TOURNAMENT_TREE

class MatchHandlerTest(TestCase):

    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=2,
            tournament_type='elimination',
            status='started',
            current_round=1,
            total_rounds=1,
            match_time=10
        )
        self.loser = Player.objects.create(avatar='C://path/my_img.jpg', name='Bowser')
        self.winner = Player.objects.create(avatar='C://path/my_img.jpg', name='Shy guy')
        self.position = Position.objects.create(
            depth=0,
            votes=0,
            tournament=self.tournament
        )
        self.position.right_position = Position.objects.create(
            depth=1,
            votes=1,
            tournament=self.tournament,
            player=self.loser
        )
        self.position.left_position = Position.objects.create(
            depth=1,
            votes=3,
            tournament=self.tournament,
            player=self.winner
        )
        self.position.save()

    def test_end_matchs_handler(self):
        pass

    def test_create_brackets_handler(self):
        tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=8,
            tournament_type='elimination',
            status='draft',
            match_time=300
        )
        handler = CreateBracketsHandler(tournament)
        handler.execute()

        tournament.refresh_from_db()
        self.assertEqual(tournament.position_set.count(), len(SIZE_8_TOURNAMENT_TREE))

    def test_start_matches_handler(self):
        pass