from rest_framework import serializers
from .models import Tournament, Player, Position, Match
from eliminationtournaments.handlers.create_brackets_handler import CreateBracketsHandler

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'avatar', 'name')

class PositionSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(required=False)  
    next_position = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    depth = 1
    class Meta:
        model = Position
        fields = ('id', 'bracket_index', 'depth', 'votes', 'player', 'next_position', 'left_position', 'right_position')
        
    def update(self, instance, validated_data):
        player_data = validated_data.pop('player')

        if player_data is not None:
            player, _ = Player.objects.get_or_create(**player_data)
            if player != instance.player:
                instance.player = player
                instance.save()
        return super().update(instance, validated_data)
        

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    position_set = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'status', 'tournament_type',
                  'current_round', 'total_rounds', 'match_time', 'match_ends',
                  'position_set')
    
    
    def create(self, data):
        instance = super().create(data)
        create_brackets = CreateBracketsHandler(instance)
        create_brackets.execute()
        instance.refresh_from_db()
        return instance
    
    def get_position_set(self, instance):
        positions = instance.position_set.all().order_by('bracket_index')
        return PositionSerializer(positions, many=True, read_only=True).data

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    position_one = PositionSerializer(read_only=True)
    position_two = PositionSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ('position_one', 'position_two' 'disabled', 'voted', 'round')
