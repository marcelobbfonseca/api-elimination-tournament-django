from rest_framework.viewsets import ModelViewSet
from eliminationtournaments.models import Player
from eliminationtournaments.serializers import PlayerSerializer

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer