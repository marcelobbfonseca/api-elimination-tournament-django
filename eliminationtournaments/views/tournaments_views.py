from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request

from eliminationtournaments.models import Tournament, TOURNAMENT_STATUS
from eliminationtournaments.serializers import TournamentSerializer

class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.order_by('-views')
    serializer_class = TournamentSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)

        if status and status in TOURNAMENT_STATUS:
            return Tournament.objects.filter(status=status).order_by('-views')
        return super().get_queryset()
