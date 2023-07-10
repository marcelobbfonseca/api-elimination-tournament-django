from rest_framework.viewsets import ModelViewSet
from eliminationtournaments.models import Tournament
from eliminationtournaments.serializers import TournamentSerializer

class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
