class Stats:
    def __init__(self, overall: int):
        self.overall: int = overall


class Player:
    def __init__(self, name: str, full_name: str, age: int, ID: int, foot: str,
                 height: int, weight: int, team: str, nation: str, stats: Stats):
        self.name: str = name
        self.full_name: str = full_name
        self.age: int = age
        self.ID: int = ID
        self.foot: str = foot
        self.height: int = height
        self.weight: int = weight
        self.team: str = team
        self.nationality: str = nation
        self.stats: Stats = stats
