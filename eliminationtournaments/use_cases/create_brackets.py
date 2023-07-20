
from eliminationtournaments.models_interfaces import TournamentInterface, PositionInterface


SIZE_8_TOURNAMENT_ROOT = '14'
SIZE_8_TOURNAMENT_TREE = {
    '14': ('12','13'),
    '12': ('8','9'),
    '13': ('10','11'),
    '8': ('0','1'),
    '9': ('2','3'),
    '10': ('4','5'),
    '11': ('6','7'),
    '7': (None, None),
    '6': (None, None),
    '5': (None, None),
    '4': (None, None),
    '3': (None, None),
    '2': (None, None),
    '1': (None, None),
    '0': (None, None),
}



def create_elimination_tournament_brackets_usecase(tournament: TournamentInterface):
    if tournament.size == 8:
        depth_first_search(SIZE_8_TOURNAMENT_ROOT, SIZE_8_TOURNAMENT_TREE, tournament)


def depth_first_search(node: str, tree: dict, tournament: TournamentInterface, depth=0):
    
    if node is not None:
        left_pos = depth_first_search(tree[node][0], tree, tournament, depth+1)
        right_pos = depth_first_search(tree[node][1], tree, tournament, depth+1)

        pos = PositionInterface.get_position().objects.create(
            bracket_index=int(node),
            depth=depth,
            tournament= tournament,
            left_position= left_pos,
            right_position=right_pos,
        )
        return pos
    return None