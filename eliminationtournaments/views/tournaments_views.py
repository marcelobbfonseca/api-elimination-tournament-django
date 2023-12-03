from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request

from eliminationtournaments.models import Tournament
from eliminationtournaments.serializers import TournamentSerializer

class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.order_by('-views')
    serializer_class = TournamentSerializer
