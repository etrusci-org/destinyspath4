import pathlib
import random




class DP4_String:
    def __init__(self, asset_dir: pathlib.Path, load_from: list[str], string_part_chance: dict[str, float]) -> None:
        self.asset_dir: pathlib.Path = asset_dir
        self.string_part_chance: dict[str, float] = string_part_chance
        self.string_data: dict[str, list[str]] = {}
        self.current_shell_name: str = ''

        for k in load_from:
            file: pathlib.Path = asset_dir.joinpath(f'{k}.txt')

            with open(file, 'r') as f:
                dump = f.read().strip()
                dump = dump.split('\n')
                dump = list(filter(None, dump))
                self.string_data[k] = dump


    def random_name(self, type: str) -> str:
        while True:
            parts: list[str] = []

            if type == 'deathcause':
                parts.append(random.choice(self.string_data['deathcause_text']))

            if type == 'container':
                parts.append(random.choice(self.string_data['object_prefix']) if random.random() < self.string_part_chance['container_prefix'] else None)
                parts.append(random.choice(self.string_data['container_name']))
                parts.append(random.choice(self.string_data['object_suffix']) if random.random() < self.string_part_chance['container_suffix'] else None)

            if type == 'object':
                parts.append(random.choice(self.string_data['object_prefix']) if random.random() < self.string_part_chance['object_prefix'] else None)
                parts.append(random.choice(self.string_data['object_name']))
                parts.append(random.choice(self.string_data['object_suffix']) if random.random() < self.string_part_chance['object_suffix'] else None)

            if type == 'entity':
                parts.append(random.choice(self.string_data['entity_prefix']) if random.random() < self.string_part_chance['entity_prefix'] else None)
                parts.append(random.choice(self.string_data['entity_name']))
                parts.append(random.choice(self.string_data['entity_suffix']) if random.random() < self.string_part_chance['entity_suffix'] else None)

            parts = list(filter(None, parts))

            name: str = ' '.join(parts)

            if type == 'entity' and name.lower() == self.current_shell_name.lower():
                continue

            if type != 'deathcause':
                name = name.title()

            return name
