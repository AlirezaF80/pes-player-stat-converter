import enum
from typing import Tuple

from player import Player


class PESPosition(enum.Enum):
    CF = "Centre Forward"
    RWF = "Right Wing Forward"
    SS = "Second Striker"
    LWF = "Left Wing Forward"
    AMF = "Attacking Midfielder"
    RMF = "Right Midfielder"
    CMF = "Centre Midfielder"
    LMF = "Left Midfielder"
    DMF = "Defensive Midfielder"
    RB = "Right Back"
    CB = "Centre Back"
    LB = "Left Back"
    GK = "Goalkeeper"


class PESPlayerStats:
    def __init__(self, overall: int):
        self.overall: int = overall
        self.position: PESPosition = None
        self.other_positions: Tuple = tuple()
        self.offensive_awareness: int = 40
        self.ball_control: int = 40
        self.dribbling: int = 40
        self.tight_possession: int = 40
        self.low_pass: int = 40
        self.lofted_pass: int = 40
        self.finishing: int = 40
        self.heading: int = 40
        self.place_kicking: int = 40
        self.curl: int = 40
        self.speed: int = 40
        self.acceleration: int = 40
        self.kicking_power: int = 40
        self.jump: int = 40
        self.physical_contact: int = 40
        self.balance: int = 40
        self.stamina: int = 40
        self.defensive_awareness: int = 40
        self.ball_winning: int = 40
        self.aggression: int = 40
        self.gk_awareness: int = 40
        self.gk_catching: int = 40
        self.gk_clearing: int = 40
        self.gk_reflexes: int = 40
        self.gk_reach: int = 40
        self.weak_foot_usage: int = 1
        self.weak_foot_acc: int = 1
        self.form: int = 1
        self.injury_resistance: int = 1


class PESPlayer(Player):
    def __str__(self):
        string = f"{self.full_name} - {self.stats.overall} {self.stats.position.name} - {self.age}y.o." \
                 f" - {self.nationality} - {self.team}"
        return string
