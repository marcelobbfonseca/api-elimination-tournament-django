from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class ServerTimeAPIView(APIView):

    def get(self, request: Request):
        now = timezone.now()
        return Response({ 'datetime': now.strftime("%m/%d/%Y, %H:%M:%S"), 'timestamp': now.timestamp() }, status=status.HTTP_200_OK)
      