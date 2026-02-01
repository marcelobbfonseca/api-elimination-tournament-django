from eliminationtournaments.handlers.start_matches_handler import StartMatchesHandler
from eliminationtournaments.handlers.create_brackets_handler import CreateBracketsHandler

# deprecated
def start_tournament(sender, instance, created, **kwargs):

    if instance.status == 'start':
        instance.status = 'started'
        start_matches = StartMatchesHandler(instance)
        start_matches.execute()

#deprecated
def create_brackets(sender, instance, created, **kwargs):

    if instance.status == 'draft' and created:
        create_brackets = CreateBracketsHandler()
        create_brackets.execute(instance)
