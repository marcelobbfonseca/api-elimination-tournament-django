from django.urls import re_path

from .consumers.vote_count import VoteConsumer

websocket_urlpatterns = [
    re_path(r"ws/position/(?P<position_id>\w+)/vote/$", VoteConsumer.as_asgi()),
]