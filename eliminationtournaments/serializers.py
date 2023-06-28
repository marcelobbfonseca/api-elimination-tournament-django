from rest_framework import serializers
from .models import Tournament, Player, Position


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'avatar', 'name')

class PositionSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    class Meta:
        model = Position
        fields = ('id', 'order', 'votes', 'player', 'next_position')

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    position_set = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'tournament_type',
                  'current_round', 'total_rounds', 'match_time',
                  'position_set')

