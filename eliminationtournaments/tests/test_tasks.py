from django.test import TestCase
from unittest.mock import patch, MagicMock

from eliminationtournaments.tasks import end_match, score_request, start_tournament
from eliminationtournaments.models import Tournament, Position
from eliminationtournaments.models_interfaces import TournamentStatuses

class TasksTests(TestCase):

    def setUp(self):
        self.tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=8,
            tournament_type='elimination',
            status='draft',
            current_round=0,
            total_rounds=3,
            match_time=600
        )  

    @patch("eliminationtournaments.tasks.publish_event")
    @patch("eliminationtournaments.tasks.StartMatchesHandler")
    def test_start_tournament_executes_handler_and_publishes_event(
        self, mock_handler, mock_publish
    ):
        handler_instance = MagicMock()
        mock_handler.return_value = handler_instance

        start_tournament(self.tournament.id)

        mock_handler.assert_called_once_with(tournament=self.tournament)
        handler_instance.execute.assert_called_once()
        mock_publish.assert_called_once()  

    @patch("eliminationtournaments.tasks.StartMatchesHandler")
    def test_start_tournament_retries_on_exception(self, mock_handler):
        mock_handler.side_effect = Exception("boom")

        with self.assertRaises(Exception):
            start_tournament(self.tournament.id)


class EndMatchTaskTest(TestCase):

    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Test",
            match_time=60,
            current_round=1,
            total_rounds=2,
            status=TournamentStatuses.STARTED,
        )

    @patch("eliminationtournaments.tasks.publish_event")
    @patch("eliminationtournaments.tasks.start_tournament")
    @patch("eliminationtournaments.tasks.EndMatchesHandler")
    def test_end_match_continues_tournament(
        self, mock_handler, mock_start_tournament, mock_publish
    ):
        handler_instance = MagicMock()
        mock_handler.return_value = handler_instance

        end_match(self.tournament.id)

        handler_instance.execute.assert_called_once()
        mock_start_tournament.delay.assert_called_once_with(self.tournament.id)
        mock_publish.assert_called_once()

    @patch("eliminationtournaments.tasks.publish_event")
    @patch("eliminationtournaments.tasks.EndMatchesHandler")
    def test_end_match_finishes_tournament(self, mock_handler, mock_publish):
        self.tournament.status = TournamentStatuses.ENDED
        self.tournament.save()

        end_match(self.tournament.id)

        mock_publish.assert_called_once()


class ScoreRequestTaskTest(TestCase):

    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Test",
            match_time=60,
            current_round=1,
            total_rounds=2,
            status=TournamentStatuses.STARTED,
        )

        self.position = Position.objects.create(
            tournament=self.tournament,
            votes=0,
        )

    @patch("eliminationtournaments.tasks.publish_event")
    def test_score_request_increments_votes(self, mock_publish):
        score_request(self.tournament.id, self.position.id)

        self.position.refresh_from_db()
        self.assertEqual(self.position.votes, 1)
        mock_publish.assert_called_once()

    @patch("eliminationtournaments.tasks.publish_event")
    def test_score_request_ignored_if_tournament_ended(self, mock_publish):
        self.tournament.status = TournamentStatuses.ENDED
        self.tournament.save()

        score_request(self.tournament.id, self.position.id)

        self.position.refresh_from_db()
        self.assertEqual(self.position.votes, 0)
        mock_publish.assert_not_called()