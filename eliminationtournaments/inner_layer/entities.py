from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TournamentEntity:
    id: int
    name: str
    size: int
    tournament_type: str
    status: str
    current_round: int
    total_rounds: int
    match_time: datetime = field(default_factory=datetime.now)
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    positions_ids: List[int] = field(default_factory=list) # positions = models.ManyToOneRel
    players_ids: List[int] = field(default_factory=list) # players = models.ManyToOneRel
    rounds_ids: List[int] = field(default_factory=list) # rounds = models.ManyToOneRel 

@dataclass
class RoundEntity:
    id: int
    round_number: int
    tournament_id: int #foreignKey
    matches_ids: List[int] = field(default_factory=list)# matches = models.ManyToOneRel


@dataclass
class MatchEntity:
    id: int
    position_one: int = field(default=None)
    position_two: int = field(default=None)
    disabled: bool = field(default=False)
    round: int = field(default=None)

@dataclass
class PlayerEntity:
    id: int
    avatar: str
    name: str

@dataclass
class PositionEntity:
    id: int
    order: int
    votes: int = field(default=0)
    tournament: int = field(default_factory=None) # models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player: int = field(default_factory=None)
    next_position: int = field(default_factory=None)
