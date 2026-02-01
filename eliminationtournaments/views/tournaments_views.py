from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from eliminationtournaments.models import Tournament
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.serializers import TournamentSerializer
from eliminationtournaments.tasks import start_tournament

class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.order_by('-views')
    serializer_class = TournamentSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)

        if status and status in TournamentStatuses.ALL:
            return Tournament.objects.filter(status=status).order_by('-views')
        return super().get_queryset()

    
    @action( detail=True,methods=["put"], url_path="start" ) # permission_classes=[IsAdminUser],
    def start(self, request, pk=None):
        tournament = self.get_object()

        # Guardrail (fast fail)
        if tournament.status != TournamentStatuses.CREATED:
            return Response(
                {"error": "Tournament cannot be started in its current state"},
                status=status.HTTP_409_CONFLICT,
            )

        # Delegate orchestration to Celery
        start_tournament.delay(tournament.id)

        return Response(
            {"message": "Tournament start scheduled"},
            status=status.HTTP_202_ACCEPTED,
        )