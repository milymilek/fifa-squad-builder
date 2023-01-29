from dataclasses import dataclass
from typing import List


@dataclass
class Player:
    name: str
    nationality: str
    club: str
    league: str
    positions: List[str]
    overall: int
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physic: int
    gk_div: int
    gk_hand: int
    gk_kick: int
    gk_pos: int
    gk_ref: int
    gk_speed: int
    assigned_position: int

    def __eq__(self, p):
        return self.name == p.name and self.club == p.club and self.league == p.league
