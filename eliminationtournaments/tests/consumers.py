import json
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase, WebsocketCommunicator
from asgiref.testing import ApplicationCommunicator
from eliminationtournaments.models import Position, Tournament
from eliminationtournaments.consumers.vote_count import VoteConsumer

class VoteConsumerTests(ChannelsLiveServerTestCase):

    def setUp(self) -> None:
        self.tournament = Tournament.objects.create()
        self.position = Position.objects.create(
            depth=1,
            votes=0,
            tournament=self.tournament
        )

        return super().setUp()

    async def test_vote_consumer(self):
        # Connect to the WebSocket
        communicator = WebsocketCommunicator(VoteConsumer.as_asgi(), "/testws/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send a message to the consumer
        await communicator.send_json_to({"hello": "word", "position_id": str(self.position.id)})

        # # Receive the response from the consumer
        response = await communicator.receive_json_from()
        
        # # Check the response from the consumer
        self.assertIsNotNone(response)

        # # Check that the position's votes have been incremented
        self.assertEqual(self.position.votes+1, response['position']['votes'])


    async def connect_ws(self):
        # Connect to the WebSocket
        channel_layer = get_channel_layer()
        connected, _ = await channel_layer.group_add("test_group", self.channel_name)
        self.assertTrue(connected)
