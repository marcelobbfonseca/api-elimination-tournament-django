from eliminationtournaments.models_interfaces import PlayerInterface, PositionInterface


def calculate_winner_usecase(position: PositionInterface) -> PlayerInterface:
    if position.left_position.votes >= position.right_position.votes:
        return position.left_position.player
    return position.right_position.player
