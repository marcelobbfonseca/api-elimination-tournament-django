from unittest import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TournamentIntegrationTest(APITestCase):

    def test_list_tournaments(self):
        # import pdb; pdb.set_trace()
        # print('hello')
        url = reverse('tournament')
        response = self.client.get(url)
        self.assertEqual(response.status, status.HTTP_200_OK)
    
    # def test_create_tournament(self):
    #     pass

    # def test_get_tournament_by_id(self):
    #     pass

