from rest_framework import serializers
from .models import Tournament, Player, Position, Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'avatar', 'name')

class PositionSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)  
    next_position = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    # next = PositionSerializer(read_only=True, required=False, source='next_position')
    depth = 1
    class Meta:
        model = Position
        fields = ('id', 'order', 'votes', 'player', 'next_position', 'left_position', 'right_position')

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    position_set = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'tournament_type',
                  'current_round', 'total_rounds', 'match_time',
                  'position_set')

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    position_one = PositionSerializer(read_only=True)
    position_two = PositionSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ('position_one', 'position_two' 'disabled', 'voted', 'round')
