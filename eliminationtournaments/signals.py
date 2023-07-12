from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler


def start_tournament(sender, instance, created, **kwargs):

    if instance.status == 'start':
        instance.status = 'started'
        start_matches = StartMatchesHandler()
        start_matches.execute(instance)
