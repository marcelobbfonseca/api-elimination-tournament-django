from rest_framework.viewsets import ModelViewSet

from eliminationtournaments.models import Tournament
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.serializers import TournamentSerializer

class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.order_by('-views')
    serializer_class = TournamentSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)

        if status and status in TournamentStatuses.ALL:
            return Tournament.objects.filter(status=status).order_by('-views')
        return super().get_queryset()
