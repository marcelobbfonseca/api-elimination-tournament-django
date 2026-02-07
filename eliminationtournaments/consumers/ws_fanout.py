from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from eliminationtournaments.events.idempotency import is_event_processed, mark_event_processed

@shared_task(
    bind=True,
    name="eliminationtournaments.consumers.ws_fanout",
)
def ws_fanout(self, event: dict):
    """
    Receives tournament.<id>.<event> messages
    and fans them out to WebSocket clients.
    """
    print(f"WS_FANOUT_TASK_EXECUTED {event}")
    
    event_id = event.get("event_id")
    if not event_id: 
        print("event is None")
        return False
    
    if is_event_processed(event_id):
        print("event is processed")
        return False

    tournament_id = event["tournament_id"]

    channel_layer = get_channel_layer()

    # One WS group per tournament
    group_name = f"tournament_{tournament_id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "tournament.event",
            "payload": event,
        },
    )

    mark_event_processed(event_id)
    return True