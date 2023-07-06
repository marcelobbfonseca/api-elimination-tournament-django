from django.test import TestCase
from eliminationtournaments.models import Tournament, Round, Player, Position, Match
from eliminationtournaments.inner_layer.entities import TournamentEntity

class TournamentTest(TestCase):
  def test_create(self):
    tournament = Tournament.objects.create(
      name='Bboy BC One',
      size=8,
      tournament_type='elimination',
      status='draft',
      current_round=0,
      total_rounds=3,
      match_time=600
      )  
    self.assertIsNotNone(tournament.id)

  def test_to_entity(self):
    tournament = Tournament.objects.create(
      name='Bboy BC One',
      size=8,
      tournament_type='elimination',
      status='draft',
      current_round=0,
      total_rounds=3,
      match_time=600
      )  
    entity: TournamentEntity = tournament.to_entity()
    self.assertIsNotNone(entity)
    self.assertEqual(entity.name, tournament.name)
    self.assertEqual(entity.id, tournament.id)


class RoundTest(TestCase):
  def test_create(self):
    tournament = Tournament.objects.create()
    round = Round.objects.create(round_number=0, tournament=tournament)
    self.assertIsNotNone(round.id)

class PlayerTest(TestCase):
  def test_create(self):
    player = Player.objects.create(avatar='C://path/my_img.jpg', name='jogador')
    self.assertIsNotNone(player.id)

class PositionTest(TestCase):
  def test_create(self):
    tournament=Tournament.objects.create()
    position = Position.objects.create(
      order=1,
      votes=0,
      tournament=tournament
    )
    self.assertIsNotNone(position.id)

  def test_next_node(self):
    tournament=Tournament.objects.create()
    position = Position.objects.create(
      order=0,
      votes=0,
      tournament=tournament
    )
    position.right_position = Position.objects.create(
      order=1,
      votes=0,
      tournament=tournament
    )
    self.assertIsNotNone(position.right_position.next_position())
    self.assertEqual(position.right_position.next_position(), position)

class MatchTest(TestCase):
  def test_create(self):
    tournament=Tournament.objects.create()
    position = Position.objects.create(order=1, votes=0, tournament=tournament)
    position_2 = Position.objects.create(order=2, votes=0, tournament=tournament)
    round = Round.objects.create(round_number=0, tournament=tournament)
    matchup = Match.objects.create(
        position_one=position,
        position_two=position_2,
        disabled=False,
        round=round
    )
    self.assertIsNotNone(matchup.id)
