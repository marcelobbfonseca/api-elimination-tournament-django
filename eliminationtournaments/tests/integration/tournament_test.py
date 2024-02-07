from eliminationtournaments.models import Tournament
from eliminationtournaments.views.views_wrappers import TournamentViewWrapper

# from unittest import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TournamentIntegrationTest(APITestCase):

    # def test_list_tournaments(self):
    #     url = reverse('tournament-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tournament_by_id(self):
        tour = Tournament.objects.create(name='tournament', size=8, tournament_type='test')
        url = reverse('tournament-details', kwargs={'id':tour.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_create_tournament(self):
    #     pass



