from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from eliminationtournaments.models import Tournament, Position, Player
from eliminationtournaments.serializers import TournamentSerializer
from eliminationtournaments.use_cases.create_brackets import SIZE_8_TOURNAMENT_TREE


class TournamentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some sample tournaments
        self.tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=8,
            tournament_type='elimination',
            status='draft',
            current_round=0,
            total_rounds=3,
            match_time=600
        )

        self.player = Player.objects.create(
            name='jogador',
            avatar='https://avatars.akamai.steamstatic.com/4cda3313aa54c29473c338196b78e9898f0b7753_full.jpg'
        )

        self.player.position_set.create(
            depth=0,
            votes=0,
            tournament=self.tournament
        )

    def test_get_tournaments(self):
        # Send a GET request to the tournaments endpoint
        response = self.client.get('/api/v2/tournaments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        tournaments_data = response.data
        tournaments = Tournament.objects.all()
        expected_data = TournamentSerializer(tournaments, many=True).data
        self.assertEqual(tournaments_data, expected_data)

    def test_retrieve_tournaments(self):
        url = '/api/v2/tournaments/' + str(self.tournament.id) + '/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tournament = Tournament.objects.get(pk=self.tournament.id)
        expected_data = TournamentSerializer(tournament).data
        self.assertEqual(expected_data, response.data)

    def test_create_tournament(self):
        tournament_data = { 'name': 'unamed tournament'}

        response = self.client.post('/api/v2/tournaments/', tournament_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_tournament = Tournament.objects.get(pk=response.data['id'])

        self.assertEqual(created_tournament.name, tournament_data['name'])
        self.assertEqual(created_tournament.position_set.count(), len(SIZE_8_TOURNAMENT_TREE))


class PositionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tournament = Tournament.objects.create(
            name='Bboy BC One',
            size=8,
            tournament_type='elimination',
            status='draft',
            current_round=0,
            total_rounds=3,
            match_time=600
        )

        self.player = Player.objects.create(
            name='jogador',
            avatar='C://avatar.png'
        )

        self.position = Position.objects.create(
            depth=0,
            votes=0,
            tournament=self.tournament
        )
    def test_update_position(self):
        player_data = { 'name': 'jogador', 'avatar': 'C://avatar.png' }
        position_data = { 'id': self.position.id, 'player': player_data, 'votes': 2 }
        url = '/api/v2/positions/' + str(self.position.id)  + '/'

        response = self.client.put(url, position_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        position = Position.objects.get(pk=self.position.id)

        self.assertEqual(position.player, self.player)


    def test_update_position_create_player(self):
        player_data = { 'name': 'novo jogador', 'avatar': 'C://avatar_2.png' }
        position_data = { 'id': self.position.id, 'player': player_data, 'votes': 2 }
        url = '/api/v2/positions/' + str(self.position.id)  + '/'

        response = self.client.put(url, position_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        position = Position.objects.get(pk=self.position.id)

        self.assertIsNotNone(position.player)
        self.assertIsNotNone(position.player.id)
        self.assertNotEqual(position.player.id, self.player.id)


class ServerTimeTest(TestCase):

    def test_get_server_time(self):
        client = APIClient()
        response = client.get('/api/v2/time/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIsNotNone(response.data['datetime'])
        self.assertIsNotNone(response.data['timestamp'])

# class IndexTest(TestCase):
#     def test_get_index(self):
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'index.html')
