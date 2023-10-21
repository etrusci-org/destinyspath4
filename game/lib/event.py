import random




class DP4_Event:
    difficulty: float
    roll: float
    win: bool
    group: str


    def __init__(self, event_group_chance: dict[str, float]) -> None:
        self.event_group_chance = event_group_chance


    def new(self) -> None:
        self.difficulty = random.random()
        self.roll = random.random()
        self.win = self.roll < self.difficulty

        for k, v in self.event_group_chance.items():
            if self.roll < v:
                self.group = k
                break
