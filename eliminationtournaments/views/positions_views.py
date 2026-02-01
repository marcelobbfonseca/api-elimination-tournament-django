from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from eliminationtournaments.models import Position
from eliminationtournaments.serializers import PositionSerializer
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.tasks import score_request
class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionAPIView(APIView):

    def put(self, request: Request, id=None):
        if id is not None:
            position = Position.objects.get(id=id)
            position.votes += 1
            position.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


    @action( detail=True,methods=["put"], url_path="score" ) # permission_classes=[IsAdminUser],
    def start(self, request, pk=None):
        position = self.get_object()
        
        # Guardrail (fast fail)
        if position.tournament.status != TournamentStatuses.CREATED:
            return Response(
                {"error": "Tournament cannot be started in its current state"},
                status=status.HTTP_409_CONFLICT,
            )

        # Delegate orchestration to Celery
        score_request.delay(position.tournament.id, position.id)

        return Response(
            {"message": "Tournament start scheduled"},
            status=status.HTTP_202_ACCEPTED,
        )