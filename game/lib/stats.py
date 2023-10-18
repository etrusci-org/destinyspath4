import json
import pathlib




class DP4_Stats:
    file: pathlib.Path


    def __init__(self, file: pathlib.Path) -> None:
        self.file = file

        self.total_distance_traveled: float = 0.0
        self.total_items_found: int = 0
        self.total_items_sold: int = 0
        self.total_trade_income: float = 0.0
        self.total_currency_stolen_by_hackers: float = 0.0
        self.total_items_stolen_by_foes: int = 0
        # self.total_kills: int = 0
        # self.total_deaths: int = 0
        # self.total_deaths_by_foes: int = 0
        # self.total_random_deaths: int = 0


    def load(self) -> None:
        if not self.file.is_file():
            return

        try:
            with open(self.file, 'r') as f:
                dump: dict[str, any] = json.loads(f.read())

                for k, v in dump.items():
                    if type(v) == type(getattr(self, k)):
                        # print('< ', k, v)
                        setattr(self, k, v)

        except Exception as e:
            print('error while loading stats data:', e)
            exit(1)


    def store(self) -> None:
        dump: dict[str, any] = {}

        for k in vars(self):
            if k == 'file': continue
            # print('> ', k, getattr(self, k))
            dump[k] = getattr(self, k)

        dump = json.dumps(dump, indent=4)

        with open(self.file, 'w') as f:
            f.write(dump)
