
from django.utils import timezone
from uuid import uuid4
from celery import shared_task
from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from eliminationtournaments.models import Tournament, Position
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.events.publisher import publish_event
from eliminationtournaments.consumers.ws_fanout import ws_fanout

@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def hello_world(self):
    try:
        return "Hello world"
    except:
        self.retry()

@shared_task(bind=True, autoretry_for=(Exception,) ,max_retries=5, default_retry_delay=30)
def start_tournament(self, tournament_id: int):
    tournament = Tournament.objects.get(id=tournament_id)
    StartMatchesHandler(tournament=tournament).execute()

    tournament.refresh_from_db()

    
    end_time = timezone.now() + timezone.timedelta(seconds=tournament.match_time)

    end_match.apply_async(
        args=[tournament.id],
        eta=end_time,
    )
    
    ws_fanout.delay({
        "event_id": str(uuid4()),
        "event_type": "start",
        "tournament_id": tournament_id,
    })


@shared_task(bind=True, autoretry_for=(Exception,), max_retries=5, default_retry_delay=30)
def end_match(self, tournament_id: int):
    tournament = Tournament.objects.get(id=tournament_id)
    EndMatchesHandler(tournament=tournament).execute()

    ws_fanout.delay({
        "event_id": str(uuid4()),
        "event_type": "end",
        "tournament_id": tournament_id,
    })

    if tournament.status != TournamentStatuses.ENDED:
        start_tournament.delay(tournament.id)



@shared_task(bind=True, autoretry_for=(Exception,), max_retries=5, default_retry_delay=30)
def score_request(self, tournament_id, position_bracket_id):
    tournament = Tournament.objects.get(id=tournament_id)
    
    if tournament.status == TournamentStatuses.ENDED:
        return
        
    pos = Position.objects.get(id=position_bracket_id)
    pos.votes+=1
    pos.save()

    ws_fanout.delay({
        "event_id": str(uuid4()),
        "event_type": "score",
        "tournament_id": tournament_id,
        "position_bracket_id": position_bracket_id,
    })
