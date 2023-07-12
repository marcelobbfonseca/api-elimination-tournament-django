from rest_framework import serializers
from .models import Tournament, Player, Position, Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'avatar', 'name')

class PositionSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)  
    next_position = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    depth = 1
    class Meta:
        model = Position
        fields = ('id', 'bracket_index', 'depth', 'votes', 'player', 'next_position', 'left_position', 'right_position')
        
class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    position_set = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'tournament_type',
                  'current_round', 'total_rounds', 'match_time', 'match_ends',
                  'position_set')
    
    def get_position_set(self, instance):
        positions = instance.position_set.all().order_by('bracket_index')
        return PositionSerializer(positions, many=True, read_only=True).data

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    position_one = PositionSerializer(read_only=True)
    position_two = PositionSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ('position_one', 'position_two' 'disabled', 'voted', 'round')
