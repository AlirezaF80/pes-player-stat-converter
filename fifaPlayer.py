import enum
from typing import Tuple

from player import Player


class FIFAPosition(enum.Enum):
    RS = "Right Striker"
    ST = "Striker"
    LS = "Left Striker"
    RW = "Right Wing Forward"
    RF = "Right Forward"
    CF = "Centre Forward"
    LF = "Left Forward"
    LW = "Left Wing Forward"
    RAM = "Right Attacking Midfielder"
    CAM = "Centre Attacking Midfielder"
    LAM = "Left Attacking Midfielder"
    RM = "Right Midfielder"
    RCM = "Right Centre Midfielder"
    CMF = "Centre Midfielder"
    LCM = "Left Centre Midfielder"
    LM = "Left Midfielder"
    RWB = "Right Wing Back"
    RDM = "Right Defensive Midfielder"
    CDM = "Center Defensive Midfielder"
    LDM = "Left Defensive Midfielder"
    LWB = "Left Wing Back"
    RB = "Right Back"
    RCB = "Right Centre Back"
    CB = "Centre Back"
    LCB = "Left Center Back"
    LB = "Left Back"
    GK = "Goalkeeper"


class FIFAPlayerStats:
    def __init__(self, overall: int):
        self.overall: int = overall
        self.position: FIFAPosition = None
        self.preferred_positions: Tuple[FIFAPosition] = tuple()
        self.ball_control: int = 10
        self.dribbling: int = 10
        self.crossing: int = 10
        self.short_pass: int = 10
        self.long_pass: int = 10
        self.gk_positioning: int = 10
        self.gk_diving: int = 10
        self.gk_handling: int = 10
        self.gk_kicking: int = 10
        self.gk_reflexes: int = 10
        self.marking: int = 10
        self.slide_tackle: int = 10
        self.stand_tackle: int = 10
        self.acceleration: int = 10
        self.stamina: int = 10
        self.strength: int = 10
        self.balance: int = 10
        self.sprint_speed: int = 10
        self.agility: int = 10
        self.jumping: int = 10
        self.heading: int = 10
        self.shot_power: int = 10
        self.finishing: int = 10
        self.long_shots: int = 10
        self.curve: int = 10
        self.fk_acc: int = 10
        self.penalties: int = 10
        self.volleys: int = 10
        self.aggression: int = 10
        self.reactions: int = 10
        self.att_position: int = 10
        self.interceptions: int = 10
        self.vision: int = 10
        self.composure: int = 10
        self.weak_foot: int = 1


class FIFAPlayer(Player):
    pass
