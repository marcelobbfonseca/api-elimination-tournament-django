from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field

DEFAULT_MATCH_TIME = 300

@dataclass(frozen=True)
class TournamentEntity:
    name: str
    size: int
    tournament_type: str
    total_rounds: int
    positions_ids: List[int] = field(default_factory=list) # positions = models.ManyToOneRel
    players_ids: List[int] = field(default_factory=list) # players = models.ManyToOneRel
    rounds_ids: List[int] = field(default_factory=list) # rounds = models.ManyToOneRel 
    id: Optional[int| None] = None
    status: Optional[str] = 'draft'
    current_round: Optional[int] = 0
    match_time: Optional[int] = DEFAULT_MATCH_TIME # seconds
    created_at: Optional[datetime] = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.created_at:
            object.__setattr__(self, "created_at", datetime.now())
        if not self.tournament_type:
            object.__setattr__(self, 'tournament_type', 'elimination')
        self.validate()

    def increment_round(self):
        self.current_round + 1
        object.__setattr__(self, "current_round", self.current_round + 1)
        return self.current_round
    
    def validate(self):
        if self.tournament_type == 'elimination' and self.size == 8 and self.total_rounds == 3:
            return True
        return False



@dataclass
class RoundEntity:
    round_number: int
    tournament_id: int #foreignKey
    matches_ids: List[int] = field(default_factory=list)# matches = models.ManyToOneRel
    id: Optional[int| None] = None


@dataclass
class MatchEntity:
    position_one: int = field(default=None)
    position_two: int = field(default=None)
    disabled: bool = field(default=False)
    round_id: int | None = field(default=None)
    id: Optional[int| None] = None

@dataclass
class PlayerEntity:
    avatar: str
    name: str
    id: Optional[int| None] = None


@dataclass(frozen=True)
class PositionEntity:
    order: int
    votes: int = field(default=0)
    tournament_id: int | None = None
    next_position: int | None = None
    player_id: Optional[int | None] = None
    id: Optional[int| None] = None
