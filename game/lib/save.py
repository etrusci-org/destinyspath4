import base64
import json
import pathlib
import shutil
import time




class DP4_Save:
    def __init__(self, file: pathlib.Path) -> None:
        self.file: pathlib.Path = file
        self.data_version: int = 1
        self.first_played: float = 0.0
        self.last_saved: float = 0.0
        self.shell_name: str = ''
        self.region_level: float = 0.0
        self.region_name: str = ''
        self.hot_wallet: float = 0.0
        self.cold_wallet: float = 0.0
        self.inventory: dict[str, dict[str, any]] = {}
        self.total_distance_traveled: float = 0.0
        self.total_items_looted: int = 0
        self.total_items_sold: int = 0
        self.total_trade_income: float = 0.0
        self.total_currency_stolen_by_hackers: float = 0.0
        self.total_items_stolen_by_foes: int = 0
        self.total_kills: int = 0
        self.total_deaths: int = 0
        self.total_deaths_by_foes: int = 0
        self.total_random_deaths: int = 0


    def load(self) -> None:
        if not self.file.is_file():
            return

        try:
            with open(self.file, 'r') as f:
                dump: str = f.read()
                data: dict[str, any] = json.loads(base64.b64decode(dump).decode())

                if data['data_version'] != self.data_version:
                    current_files = self.file.parent.glob(f'{self.file.stem}.*')
                    for src in current_files:
                        dst = self.file.parent.joinpath(f'backup.{int(time.time())}.{src.name}')
                        shutil.move(src, dst)
                    return

                for k, v in data.items():
                    if type(v) == type(getattr(self, k)):
                        setattr(self, k, v)
        except Exception as e:
            print('error while loading save data:', e)
            exit(20)


    def store(self) -> None:
        self.last_saved = time.time()

        try:
            with open(self.file, 'wb') as f:
                dump: dict[str, any] = {}
                for k in vars(self):
                    if k == 'file': continue
                    dump[k] = getattr(self, k)

                out: bytes = base64.b64encode(json.dumps(dump).encode())
                f.write(out)
        except Exception as e:
            print('error while storing save data:', e)
            exit(21)
