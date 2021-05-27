import enum

from player import Stats, Player


class Position(enum.Enum):
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


class PESPlayerStats(Stats):
    def __init__(self, overall: int):
        super().__init__(overall)
        position: Position
        offensive_awareness: int
        ball_control: int
        dribbling: int
        tight_possession: int
        low_pass: int
        lofted_pass: int
        finishing: int
        heading: int
        place_kicking: int
        curl: int
        speed: int
        acceleration: int
        kicking_power: int
        jump: int
        physical_contact: int
        balance: int
        stamina: int
        defensive_awareness: int
        ball_winning: int
        aggression: int
        gk_awareness: int
        gk_catching: int
        gk_clearing: int
        gk_reflexes: int
        gk_reach: int
        weak_foot_usage: int
        weak_foot_acc: int
        form: int
        injury_resistance: int


class PESPlayer(Player):
    pass
