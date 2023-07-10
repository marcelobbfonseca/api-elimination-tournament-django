from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from eliminationtournaments.models import Position
from eliminationtournaments.serializers import PositionSerializer

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