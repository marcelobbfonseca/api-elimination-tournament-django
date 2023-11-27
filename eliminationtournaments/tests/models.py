from django.test import TestCase
from eliminationtournaments.models import Tournament, Player, Position
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



class PlayerTest(TestCase):
  def test_create(self):
    player = Player.objects.create(avatar='C://path/my_img.jpg', name='jogador')
    self.assertIsNotNone(player.id)

class PositionTest(TestCase):
  def test_create(self):
    tournament=Tournament.objects.create()
    position = Position.objects.create(
      depth=1,
      votes=0,
      tournament=tournament
    )
    self.assertIsNotNone(position.id)

  def test_next_node(self):
    tournament=Tournament.objects.create()
    position = Position.objects.create(
      depth=0,
      votes=0,
      tournament=tournament
    )
    position.right_position = Position.objects.create(
      depth=1,
      votes=0,
      tournament=tournament
    )
    self.assertIsNotNone(position.right_position.next_position())
    self.assertEqual(position.right_position.next_position(), position)

