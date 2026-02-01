
from celery import shared_task
from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler
from eliminationtournaments.handlers.end_matches_handler import EndMatchesHandler
from eliminationtournaments.models import Tournament, Position
from eliminationtournaments.models_interfaces import TournamentStatuses
from eliminationtournaments.events.publisher import publish_event
from uuid import uuid4

@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def hello_world(self):
    try:
        return "Hello world"
    except:
        self.retry()

@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def start_tournament(self, tournament_id: int):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        StartMatchesHandler(tournament=tournament).execute()
       
        publish_event(
            event_id=uuid4(),
            routing_key=f"tournament.{tournament_id}.start",
            payload={
                "event_id": uuid4(),
                "tournament_id": tournament_id
            },
        )


    except Exception as exc:
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def end_match(self, tournament_id: int):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        EndMatchesHandler(tournament=tournament).execute()


        publish_event(
            event_id=uuid4(),
            routing_key=f"tournament.{tournament_id}.end",
            payload={
                "event_id": uuid4(),
                "tournament_id": tournament_id
            },
        )

        if tournament.status != TournamentStatuses.ENDED:
            start_tournament.delay(tournament.id)

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def score_request(self, tournament_id, position_bracket_id):
    tournament = Tournament.objects.get(id=tournament_id)
    
    if tournament.status == TournamentStatuses.ENDED:
        return
        
    pos = Position.objects.get(id=position_bracket_id)
    pos.votes+=1
    pos.save()

    publish_event(
        routing_key=f"tournament.{tournament_id}.position.{position_bracket_id}.score",
        payload={
            "event_id": uuid4(),
            "tournament_id": tournament_id,
            "position_bracket_id": position_bracket_id,
        },
    )
