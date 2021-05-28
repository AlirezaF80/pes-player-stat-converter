import enum
from typing import Tuple

from player import Stats, Player


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


class FIFAPlayerStats(Stats):
    def __init__(self, overall: int):
        super().__init__(overall)
        position: FIFAPosition
        preferred_positions: Tuple[FIFAPosition] = tuple()
        ball_control: int
        dribbling: int
        crossing: int
        short_pass: int
        long_pass: int
        gk_positioning: int
        gk_diving: int
        gk_handling: int
        gk_kicking: int
        gk_reflexes: int
        marking: int
        slide_tackle: int
        stand_tackle: int
        acceleration: int
        stamina: int
        strength: int
        balance: int
        sprint_speed: int
        agility: int
        jumping: int
        heading: int
        shot_power: int
        finishing: int
        long_shots: int
        curve: int
        fk_acc: int
        penalties: int
        volleys: int
        aggression: int
        reactions: int
        att_position: int
        interceptions: int
        vision: int
        composure: int
        weak_foot_acc: int


class FIFAPlayer(Player):
    pass
