import json
from eliminationtournaments.models_interfaces import PositionInterface
from eliminationtournaments.serializers import PositionSerializer

from channels.generic.websocket import WebsocketConsumer


class VoteConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        position_id = text_data_json["position_id"]

        # Find Position by ID
        Position = PositionInterface.get_position()
        position = Position.objects.get(id=int(position_id))
        
        # increment position vote
        position.increment_vote()
        position.save()

        # Return incremented position
        position_json = PositionSerializer(position).data
        self.send(text_data=json.dumps({"message": 'vote!', 'position': position_json}))

        