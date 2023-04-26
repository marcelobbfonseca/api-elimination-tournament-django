from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        # 'positions', 'players', 'rounds'
        fields = ('id', 'name', 'status', 'tournament_type', 'current_round', 'total_rounds', 'match_time',)

