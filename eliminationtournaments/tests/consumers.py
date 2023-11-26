import json
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase, WebsocketCommunicator
from asgiref.testing import ApplicationCommunicator
from eliminationtournaments.models import Position, Tournament
from eliminationtournaments.consumers.vote_notification import NotifyVoteConsumer 



class NotifyVoteConsumerTest(ChannelsLiveServerTestCase):

    def setUp(self) -> None:
        self.tournament = Tournament.objects.create()
        self.position = Position.objects.create(
            depth=1,
            votes=0,
            tournament=self.tournament
        )

        return super().setUp()


    async def test_connect(self):

        communicator = WebsocketCommunicator(NotifyVoteConsumer.as_asgi(), "ws/tournament/1/position/vote/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    async def test_receive(self):
        communicator = WebsocketCommunicator(NotifyVoteConsumer.as_asgi(), "ws/tournament/1/position/vote/")
        await communicator.connect()

        # Send a message to the consumer
        await communicator.send_json_to({"positionId": str(self.position.id)})

        # Receive the response from the consumer
        response = await communicator.receive_json_from()
        # Check the response from the consumer
        self.assertIsNotNone(response)

        # # Check that the position's votes have been incremented
        self.assertEqual(self.position.id, int(response['positionId']))
