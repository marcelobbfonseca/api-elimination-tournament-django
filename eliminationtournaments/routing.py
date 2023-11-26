from django.urls import re_path

from .consumers.vote_notification import NotifyVoteConsumer

websocket_urlpatterns = [
    re_path(r"ws/tournament/(?P<tournament_id>\w+)/position/vote/$", NotifyVoteConsumer.as_asgi()),
]