from eliminationtournaments.views import TournamentView

from typing import Any
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from eliminationtournaments.models import Tournament, Player, Position
from eliminationtournaments.serializers import TournamentSerializer, PlayerSerializer, PositionSerializer

class TournamentViewWrapper(APIView):

    def __init__(self, **kwargs: Any) -> None:
        self.view = TournamentView()
        super().__init__(**kwargs)

    def post(self, request: Request, *args, **kwargs):
        response = self.view.create(request.POST)
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request: Request, id=None):
        if id is not None:
            response = self.view.retrieve(id) 
        else: 
            response = self.view.list()

        return Response(response, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        response = self.view.update(request.POST, id)
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request: Request, id=None):
        response = self.view.delete(id)
        return Response(response, status=status.HTTP_200_OK)



class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

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