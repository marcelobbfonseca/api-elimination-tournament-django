from unittest.mock import patch, MagicMock, AsyncMock

from django.test import TestCase
from django.core.cache import cache

from eliminationtournaments.consumers.ws_fanout import ws_fanout


class WSFanoutExactOnceTest(TestCase):
    def setUp(self):
        cache.clear()

        self.valid_event = {
            "event_id": "evt-123",
            "tournament_id": 1,
            "position_bracket_id": 10,
            "votes": 3,
            "event_type": "score",
        }

    @patch("eliminationtournaments.consumers.ws_fanout.get_channel_layer")
    def test_sends_event_once(self, mock_get_channel_layer):
        mock_layer = MagicMock()
        mock_layer.group_send = AsyncMock()
        mock_get_channel_layer.return_value = mock_layer

        ws_fanout(self.valid_event)

        mock_layer.group_send.assert_awaited_once_with(
            "tournament_1",
            {"type": "tournament.event", "payload": self.valid_event},
        )

    @patch("eliminationtournaments.consumers.ws_fanout.get_channel_layer")
    def test_duplicate_event_is_ignored(self, mock_get_channel_layer):
        mock_layer = MagicMock()
        mock_layer.group_send = AsyncMock()
        mock_get_channel_layer.return_value = mock_layer

        ws_fanout(self.valid_event)
        ws_fanout(self.valid_event)

        mock_layer.group_send.assert_awaited_once()

    @patch("eliminationtournaments.consumers.ws_fanout.get_channel_layer")
    def test_event_without_event_id_is_ignored(self, mock_get_channel_layer):
        mock_layer = MagicMock()
        mock_layer.group_send = AsyncMock()
        mock_get_channel_layer.return_value = mock_layer

        ws_fanout({"tournament_id": 1})

        mock_layer.group_send.assert_not_awaited()
