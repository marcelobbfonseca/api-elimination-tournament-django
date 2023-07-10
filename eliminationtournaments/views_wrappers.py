from eliminationtournaments.views.v1_views import TournamentView

from typing import Any
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

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



