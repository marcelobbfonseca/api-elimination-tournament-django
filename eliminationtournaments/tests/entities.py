# from django.test import TestCase
from eliminationtournaments.inner_layer.entities import (TournamentEntity, DEFAULT_MATCH_TIME,
    RoundEntity, MatchEntity, PlayerEntity, PositionEntity)
from unittest import TestCase
from unittest.mock import patch


class TournamentEntityTest(TestCase):
    def test_constructor(self):
        with patch.object(TournamentEntity, 'validate') as mock_validate_method:
            tournament = TournamentEntity('My Tournament', 8, 'elimination', 3, [], [], [])
            mock_validate_method.assert_called_once()
            self.assertEqual(tournament.name, 'My Tournament')
            self.assertEqual(tournament.size, 8)
            self.assertEqual(tournament.tournament_type, 'elimination')
            self.assertEqual(tournament.total_rounds, 3)
            self.assertEqual(tournament.match_time, DEFAULT_MATCH_TIME)
            self.assertEqual(tournament.status, 'draft')

class RoundEntityTest(TestCase):
    def test_constructor(self):
        round = RoundEntity(0, 304, [])
        self.assertEqual(round.round_number, 0)
        self.assertEqual(round.tournament_id, 304)
        self.assertEqual(len(round.matches_ids), 0)

class MatchEntityTest(TestCase):
    def test_constructor(self):
        matchup = MatchEntity(2, 3)
        self.assertEqual(matchup.position_one, 2)
        self.assertEqual(matchup.position_two, 3)
        self.assertEqual(matchup.disabled, False)
        self.assertEqual(matchup.round_id, None)
        

class PlayerEntityTest(TestCase):
    def test_constructor(self):
        player = PlayerEntity('C://images/avatar.jpg', 'Rei Kuduro')
        self.assertEqual(player.avatar, 'C://images/avatar.jpg')
        self.assertEqual(player.name, 'Rei Kuduro')
        self.assertEqual(player.id, None)

class PositionEntityTest(TestCase):
    def test_constructor(self):
        position = PositionEntity(0, 0, 402)
        self.assertEqual(position.order, 0)
        self.assertEqual(position.votes, 0)
        self.assertEqual(position.id, None)
        self.assertEqual(position.player_id, None)
        self.assertEqual(position.tournament_id, 402)
        self.assertEqual(position.next_position, None)
