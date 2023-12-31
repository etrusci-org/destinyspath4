import argparse
import base64
import datetime
import json
import pathlib
import random
import sys
import time
import logging

from .conf import DP4_Conf
from .event import DP4_Event
from .lang import DP4_Lang
from .string import DP4_String
from .save import DP4_Save
from .terminal import clear_terminal
from .terminal import disable_terminal_cursor
from .terminal import enable_terminal_cursor
from .spinner import spinner
from .number import rffr
from .number import ff




class DP4_Core:
    def __init__(self) -> None:
        self.Conf: DP4_Conf = DP4_Conf()
        self.Event: DP4_Event = DP4_Event(event_group_chance=self.Conf.event_group_chance)
        self.String: DP4_String = DP4_String(asset_dir=self.Conf.asset_dir, load_from=self.Conf.string_load_from, string_part_chance=self.Conf.string_part_chance)
        self.CLIParser: argparse.ArgumentParser = argparse.ArgumentParser(
            description=f'''
                An idle-game that is *played* in the terminal. No user input is necessary when it runs. Everything that happens depends on your luck.
                Quit by pressing CTRL+C. For detailed help see the README.
            ''',
            epilog='Made by arT2 (etrusci.org). Repository: https://github.com/etrusci-org/destinyspath4',
        )

        self.CLIParser.add_argument('-p', '--play',
            action='store_true',
            help='play the game',
        )

        self.CLIParser.add_argument('-s', '--list-saves',
            action='store_true',
            help='list save data info from the current save data directory',
        )

        self.CLIParser.add_argument('-n', '--save-name',
            metavar='<NAME>',
            type=str,
            default=self.Conf.save_name,
            required=False,
            help=f'name of the save game to create or resume from',
        )

        self.CLIParser.add_argument('-d', '--save-dir',
            metavar='<PATH>',
            type=str,
            default=self.Conf.save_dir,
            required=False,
            help=f'path to the save data directory',
        )

        self.CLIParser.add_argument('-i', '--autosave-interval',
            metavar='<SECONDS>',
            type=int,
            default=self.Conf.autosave_interval,
            required=False,
            help=f'time in seconds on which the progress should automatically be saved to file',
        )

        self.CLIParser.add_argument('-f', '--log-to-file',
            action='store_true',
            help=f'write progress lines to log file',
        )

        # lang option disabled until there is a second translation
        # self.CLIParser.add_argument('-t', '--translation',
        #     metavar='LANGCODE',
        #     type=str,
        #     default=self.Conf.lang,
        #     choices=self.Conf.lang_list,
        #     required=False,
        #     help=f'translation to use for output (choose from: {"|".join(self.Conf.lang_list)}, default={self.Conf.lang})'
        # )

        self.cliargs: argparse.Namespace = self.CLIParser.parse_args()

        save_dir: pathlib.Path = pathlib.Path(self.cliargs.save_dir).resolve()
        if not save_dir.exists() or not save_dir.is_dir():
            self.log(f'--save-dir does not exist or is not a directory: {save_dir}', sleep=0, to_file=False)
            exit(1)

        # all peaches and cream if we reach this line
        self.Conf.save_dir = save_dir
        self.Conf.save_name = self.cliargs.save_name
        self.Conf.save_file = self.Conf.save_dir.joinpath(f'{self.Conf.save_name}.dp4')
        self.Conf.autosave_interval = self.cliargs.autosave_interval

        self.Save = DP4_Save(file=self.Conf.save_file)

        # self.Conf.lang = self.cliargs.translation
        self.Lang: DP4_Lang = DP4_Lang(lang_code=self.Conf.lang)

        self.Conf.log_to_file = self.cliargs.log_to_file
        self.Conf.log_file = self.Conf.save_dir.joinpath(f'{self.Conf.save_name}.log')
        self.prev_log_msg: str = ''

        if self.Conf.log_to_file:
            logging.basicConfig(
                filename=self.Conf.log_file,
                level=logging.DEBUG,
                format='%(asctime)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            )


    # -----------------------------------------------------------------------


    def play(self) -> None:
        try:
            clear_terminal()
            disable_terminal_cursor()

            self.log(f'Initializing save data "{self.Conf.save_name}"', sleep=0, to_file=False)
            self.log(f'file: {self.Save.file}', sleep=0, to_file=False)
            spinner(3, type='binary', start='\n', end='')

            self.Save.load()

            self.log(f'Initializing world', sleep=0, to_file=False)
            spinner(3, type='binary', start='\n', end='')

            self.init_world_files()

            if self.Save.first_played == 0:
                self.Save.first_played = time.time()
                self.Save.region_name = self.String.region_name(self.Save.region_level)
                self.Save.shell_name = self.String.random_name('entity')
                self.log('Starting new game', sleep=0)
            else:
                self.log('Resuming game', sleep=0)

            spinner(4, type='binary', start='\n')

            self.String.current_shell_name = self.Save.shell_name # set current shell name in string class to avoid having the same name after a restart/rebirth

            self.game_loop()
        except KeyboardInterrupt:
            exit(0)
        finally:
            self.Save.store()
            self.log('Quitting game', start='\n\n', sleep=0)
            self.log(f'Progress saved to {self.Save.file}', sleep=0, to_file=False)
            enable_terminal_cursor()


    def game_loop(self) -> None:
        is_first_iter: bool = True
        self.game_loop_iter_count: int = 0

        while True:
            clear_terminal()
            disable_terminal_cursor()

            self.print_head()

            self.simulate_event(is_first_iter)

            spinner(rffr(self.Conf.end_of_gameloop_duration), type='binary', start='\n', end='')

            if not is_first_iter and time.time() - self.Save.last_saved > self.Conf.autosave_interval:
                self.Save.store()

            is_first_iter = False
            self.game_loop_iter_count += 1


    def simulate_event(self, is_first_iter: bool) -> None:
        if is_first_iter:
            self.sim_wakeup()
            return

        if len(self.Save.inventory.keys()) >= self.Conf.inventory_size:
            self.sim_sell()
            return

        if self.Save.hot_wallet > self.Conf.sim_transfer_currency_treshold:
            self.sim_transfer_currency()
            return

        while True:
            clear_terminal()
            self.print_head()
            self.sim_walk()
            if random.random() < self.Conf.sim_walk_startevent_chance:
                clear_terminal()
                break

        self.print_head()

        self.Event.new()
        if self.Event.group == 'death': self.sim_death()
        if self.Event.group == 'gift': self.sim_gift()
        if self.Event.group == 'hacker': self.sim_hacker()
        if self.Event.group == 'container': self.sim_container()
        if self.Event.group == 'entity': self.sim_entity()


    # -----------------------------------------------------------------------


    def sim_wakeup(self) -> None:
        self.log(self.Lang.sim_wakeup.format(shell_name=self.Save.shell_name), sleep=rffr(self.Conf.sim_wakeup_wakingup_duration), with_spinner=True)


    def sim_walk(self) -> None:
        start = time.time()

        self.log(self.Lang.sim_walk, sleep=rffr(self.Conf.sim_walk_walking_duration), with_spinner=True, spinner_type='arrow')

        self.update_distance_traveled(start)

        prev_region_level: int = int(self.Save.region_level)

        self.update_region_level()

        if int(self.Save.region_level) != prev_region_level:
            self.log(self.Lang.sim_walk_enternewregion.format(region_name=self.Save.region_name, region_level=int(self.Save.region_level)), sleep=rffr(self.Conf.sim_walk_enternewregion_duration), with_spinner=True, spinner_type='arrow')


    def sim_sell(self) -> None:
        self.log(self.Lang.sim_sell_wagonfull)
        self.log(self.Lang.sim_sell_lookingforvendor, sleep=rffr(self.Conf.sim_sell_searchvendor_duration), with_spinner=True)

        vendor_name = self.String.random_name('entity')
        self.log(self.Lang.sim_sell_foundshop.format(vendor_name=vendor_name))

        self.log(self.Lang.sim_sell_negvendormod, sleep=rffr(self.Conf.sim_sell_negvendormod_duration), with_spinner=True)

        vendor_mod = rffr(self.Conf.sim_sell_vendormod_range)
        self.log(self.Lang.sim_sell_negvendormodresult.format(vendor_mod=ff(vendor_mod)))

        total_income: float = 0.0
        total_items_sold: int = 0

        for item_name in sorted(self.Save.inventory):
            item_count = self.Save.inventory[item_name]['count']
            item_value = self.Save.inventory[item_name]['item_value'] * vendor_mod
            stack_value = item_value * item_count

            total_income += stack_value
            total_items_sold += item_count

            self.Save.hot_wallet += stack_value

            self.Save.total_items_sold += item_count
            self.Save.total_trade_income += stack_value

            del self.Save.inventory[item_name]

            per_item_value_str = f'(1={ff(item_value)})' if item_count > 1 else ''

            self.log(self.Lang.sim_sell_solditem.format(item_count=item_count, item_name=item_name, stack_value=ff(stack_value), per_item_value=per_item_value_str, currency_name=self.Conf.currency_name))

        self.log(self.Lang.sim_sell_result.format(total_income=ff(total_income), item_count=total_items_sold, currency_name=self.Conf.currency_name))
        self.log(self.Lang.sim_sell_leavingshop, sleep=rffr(self.Conf.sim_sell_leavevendor_duration), with_spinner=True)


    def sim_transfer_currency(self) -> None:
        self.log(self.Lang.sim_transfer_currency_thresholdtriggered)

        self.log(self.Lang.sim_transfer_currency_transfering.format(currency_name=self.Conf.currency_name), sleep=rffr(self.Conf.sim_transfer_currency_transfer_duration), with_spinner=True)

        transfer_amount = self.Save.hot_wallet * self.Conf.sim_transfer_currency_transfer_amount_mod

        self.Save.cold_wallet += transfer_amount
        self.Save.hot_wallet -= transfer_amount

        self.log(self.Lang.sim_transfer_currency_result.format(transfer_amount=ff(transfer_amount), currency_name=self.Conf.currency_name))


    def sim_death(self) -> None:
        self.Save.total_deaths += 1
        self.Save.total_random_deaths += 1

        deathcause = self.String.random_name('deathcause')

        self.log(self.Lang.sim_death.format(cause_of_death=deathcause), sleep=rffr(self.Conf.sim_death_dying_duration), with_spinner=True, spinner_type='heartbeat')

        self.sim_rebirth()


    def sim_rebirth(self) -> None:
        self.log(self.Lang.sim_rebirth_waiting, sleep=rffr(self.Conf.sim_rebirth_waiting_duration), with_spinner=True)

        self.Save.shell_name = self.String.random_name('entity')
        self.String.current_shell_name = self.Save.shell_name

        self.sim_wakeup()

        self.log(self.Lang.sim_rebirth_calibrating, sleep=rffr(self.Conf.sim_rebirth_calibrate_duration), with_spinner=True, spinner_type='binary2')


    def sim_gift(self) -> None:
        self.log(self.Lang.sim_gift_strangerapproaches, sleep=rffr(self.Conf.sim_gift_approach_duration), with_spinner=True)

        if not self.Event.win:
            self.log(self.Lang.sim_gift_strangerwalksby)
            return

        self.log(self.Lang.sim_gift_yougetboxfromstranger)
        self.log(self.Lang.sim_gift_youthankstranger)
        self.log(self.Lang.sim_gift_strangernodsandwalksaway)

        self.log(self.Lang.sim_gift_youopengift, sleep=rffr(self.Conf.sim_gift_opengift_duration), with_spinner=True)

        self.sim_find_loot(count=1)


    def sim_hacker(self) -> None:
        self.log(self.Lang.sim_hacker_hackersattacking, sleep=rffr(self.Conf.sim_hacker_attack_duration), with_spinner=True)

        if self.Event.win:
            self.log(self.Lang.sim_hacker_accessfailed)
            return

        self.log(self.Lang.sim_hacker_accessgained, sleep=rffr(self.Conf.sim_hacker_hacking_duration), with_spinner=True)

        if self.Save.hot_wallet == 0:
            self.log(self.Lang.sim_hacker_walletwasempty)
            return

        stolen_amount = self.Save.hot_wallet

        self.Save.hot_wallet -= stolen_amount

        self.Save.total_currency_stolen_by_hackers += stolen_amount

        self.log(self.Lang.sim_hacker_youlostcurrency.format(stolen_amount=ff(stolen_amount), currency_name=self.Conf.currency_name))


    def sim_container(self) -> None:
        container_name = self.String.random_name('container')

        self.log(self.Lang.sim_container_findcontainer.format(container_name=container_name))

        self.log(self.Lang.sim_container_lookinside, sleep=rffr(self.Conf.sim_container_checking_duration), with_spinner=True)

        self.sim_find_loot()


    def sim_entity(self) -> None:
        entity_name = self.String.random_name('entity')

        self.log(self.Lang.sim_entity_meet.format(entity_name=entity_name))

        attitude_player: str = random.choice(self.Conf.sim_entity_attitude)
        attitude_entity: str = random.choice(self.Conf.sim_entity_attitude)

        self.log(self.Lang.sim_entity_yourfirstreaction.format(attitude_player=attitude_player), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

        if attitude_player == 'hostile':

            if attitude_entity == 'hostile':
                self.log(self.Lang.sim_entity_hostileentityreaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    self.log(self.Lang.sim_entity_youflee)
                    return
                self.log(self.Lang.sim_entity_bothattack)
                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                self.log(self.Lang.sim_entity_friendlyentityreaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_entityflee_chance_range):
                    self.log(self.Lang.sim_entity_entityflee.format(entity_name=entity_name))
                    return
                self.log(self.Lang.sim_entity_youattack.format(entity_name=entity_name))
                self.sim_fight(entity_name)

        if attitude_player == 'friendly':

            if attitude_entity == 'hostile':
                self.log(self.Lang.sim_entity_entityactshostile.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

                self.log(self.Lang.sim_entity_friendlyyoureaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    self.log(self.Lang.sim_entity_youflee)
                    return

                self.log(self.Lang.sim_entity_entityattack.format(entity_name=entity_name))

                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                if random.random() < rffr(self.Conf.sim_entity_conversation_chance_range):
                    self.log(self.Lang.sim_entity_entityisopenforcontact.format(entity_name=entity_name))
                    self.sim_conversation(entity_name)
                    return

                self.log(self.Lang.sim_entity_entitydoesnotwantcontact.format(entity_name=entity_name))


    def sim_conversation(self, entity_name: str) -> None:
        item_name = self.String.random_name('object')

        self.log(self.Lang.sim_conversation_inprogress.format(item_name=item_name), sleep=rffr(self.Conf.sim_conversation_convo_duration), with_spinner=True)

        if self.Event.win:
            self.log(self.Lang.sim_conversation_entityapproves.format(entity_name=entity_name))

            self.add_inventory_item(item_name)

            self.log(self.Lang.sim_conversation_getitem.format(item_name=item_name))
            self.log(self.Lang.sim_conversation_youthankentity.format(entity_name=entity_name))
        else:
            self.log(self.Lang.sim_conversation_entitylostinterest.format(entity_name=entity_name))

        self.log(self.Lang.sim_conversation_end)


    def sim_fight(self, entity_name: str) -> None:
        self.log(self.Lang.sim_fight_inprogress, sleep=rffr(self.Conf.sim_fight_fighting_duration), with_spinner=True)

        if not self.Event.win:
            self.Save.total_deaths += 1
            self.Save.total_deaths_by_foes += 1

            self.log(self.Lang.sim_fight_yougotkilled.format(entity_name=entity_name), spinner_type='heartbeat')

            if len(self.Save.inventory.keys()) > 0:
                stolen_items_count: int = random.randint(self.Conf.sim_fight_stolenitemsmin_count, max(1, int(len(self.Save.inventory.keys()) * self.Conf.sim_fight_stolenitemsmax_mod)))
                stolen_items: list = random.sample(sorted(self.Save.inventory), stolen_items_count)
                for item_name in stolen_items:
                    item_count = self.Save.inventory[item_name]['count']

                    self.Save.total_items_stolen_by_foes += item_count

                    del self.Save.inventory[item_name]

                    self.log(self.Lang.sim_fight_entitystealsitem.format(entity_name=entity_name, item_count=item_count, item_name=item_name))

            self.sim_rebirth()
            return

        self.Save.total_kills += 1

        self.log(self.Lang.sim_fight_youkilledentity.format(entity_name=entity_name))

        self.log(self.Lang.sim_fight_yousearchcorpse, sleep=rffr(self.Conf.sim_fight_searchcorpse_duration), with_spinner=True)

        self.sim_find_loot()

        self.log(self.Lang.sim_fight_youhidecorpse, sleep=rffr(self.Conf.sim_fight_hidecorpse_duration), with_spinner=True)


    def sim_find_loot(self, count: int = None) -> None:
        item_count: int = count if count else random.randint(*self.Conf.sim_find_loot_count)

        if item_count == 0:
            self.log(self.Lang.sim_find_loot_containerisempty)
            return

        found_items: list[str] = []

        while len(found_items) < item_count:
            item_name: str = self.String.random_name('object')
            if item_name in found_items:
                continue
            found_items.append(item_name)
            self.log(self.Lang.sim_find_loot_finditem.format(item_name=item_name))

        self.log(self.Lang.sim_find_loot_checkwagonspace, sleep=rffr(self.Conf.sim_find_loot_wagoncheck_duration), with_spinner=True)

        random.shuffle(found_items)

        for item_name in found_items:
            if len(self.Save.inventory.keys()) >= self.Conf.inventory_size and not self.Save.inventory.get(item_name):
                self.log(self.Lang.sim_find_loot_discarditem.format(item_name=item_name))
                continue
            self.log(self.Lang.sim_find_loot_storeitem.format(item_name=item_name))
            self.add_inventory_item(item_name)


    # -----------------------------------------------------------------------


    def init_world_files(self):
        prefix_dump_file: pathlib.Path = self.Conf.asset_dir.joinpath('region_prefix.dat')
        suffix_dump_file: pathlib.Path = self.Conf.asset_dir.joinpath('region_suffix.dat')
        prefix_out_file: pathlib.Path = self.Conf.save_dir.joinpath(f'{self.Conf.save_name}.rp.dat')
        suffix_out_file: pathlib.Path = self.Conf.save_dir.joinpath(f'{self.Conf.save_name}.rs.dat')

        if prefix_out_file.is_file() \
        and suffix_out_file.is_file():
            with open(prefix_out_file, 'r') as prefix_of, \
                 open(suffix_out_file, 'r') as suffix_of:
                prefix_dump = prefix_of.read().split()
                suffix_dump = suffix_of.read().split()

                self.String.string_data['region_prefix']: list[str] = prefix_dump
                self.String.string_data['region_suffix']: list[str] = suffix_dump
            return

        with open(prefix_dump_file, 'r') as prefix_df, \
            open(suffix_dump_file, 'r') as suffix_df, \
            open(prefix_out_file, 'w') as prefix_of, \
            open(suffix_out_file, 'w') as suffix_of:

            prefix_dump = prefix_df.read().split()
            suffix_dump = suffix_df.read().split()

            prefix_dump = list(filter(None, prefix_dump))
            suffix_dump = list(filter(None, suffix_dump))

            random.shuffle(prefix_dump)
            random.shuffle(suffix_dump)

            self.String.string_data['region_prefix']: list[str] = prefix_dump
            self.String.string_data['region_suffix']: list[str] = suffix_dump

            prefix_of.write('\n'.join(prefix_dump))
            suffix_of.write('\n'.join(suffix_dump))


    def update_distance_traveled(self, started_walking_on: float) -> None:
        self.Save.total_distance_traveled += self.Conf.travel_speed * ((time.time() - started_walking_on) / 3_600)


    def update_region_level(self) -> None:
        self.Save.region_level = ((((8 * (self.Save.total_distance_traveled * 100) / 100 + 1) ** 0.5) - 1) / 2)
        self.Save.region_name = self.String.region_name(self.Save.region_level)


    def add_inventory_item(self, item_name: str) -> None:
        self.Save.total_items_looted += 1

        item_value = self.item_value(item_name)

        if not self.Save.inventory.get(item_name):
            self.Save.inventory[item_name] = {
                'count': 1,
                'item_value': item_value,
                'stack_value': item_value,
            }
            return

        self.Save.inventory[item_name]['count'] += 1
        self.Save.inventory[item_name]['stack_value'] = item_value * self.Save.inventory[item_name]['count']


    def item_value(self, item_name: str) -> float:
        item_value: float = len(item_name) * self.Conf.item_base_value_mod

        for char in item_name.lower():
            item_value += self.Conf.item_name_char_value.get(char, self.Conf.item_name_unknown_char_value)

        return item_value


    # -----------------------------------------------------------------------


    def list_saves(self) -> None:
        dump = list(self.Conf.save_dir.glob('*.dp4'))

        if len(dump) == 0:
            self.log(f'No save data files found in: {self.Conf.save_dir}', sleep=0, to_file=False)
            self.log(f'Try --play first', sleep=0, to_file=False)
            return

        self.log(f'Listing save data files from: {self.Conf.save_dir}', sleep=0, with_spinner=True, to_file=False)
        self.log('', sleep=0, to_file=False)
        self.log('Resume any of these games with --save-name <NAME>', sleep=0, to_file=False)
        self.log(f'e.g.: dp4.py --play --save-name {dump[0].stem}', sleep=0, to_file=False)

        for file in sorted(dump):
            with open(file, 'r') as f:
                dump: str = f.read()
                data: dict[str, any] = json.loads(base64.b64decode(dump).decode())
                self.log('', sleep=0, to_file=False)
                self.log(f'        name: {file.stem}', sleep=0, to_file=False)
                self.log(f'        file: {file}', sleep=0, to_file=False)
                self.log(f'first played: {datetime.datetime.fromtimestamp(int(data["first_played"])) if data["first_played"] > 0 else "never"}', sleep=0, to_file=False)
                self.log(f'  last saved: {datetime.datetime.fromtimestamp(int(data["last_saved"]))}', sleep=0, to_file=False)


    # -----------------------------------------------------------------------


    def log(self, msg: str = '', start: str = '', end: str = '\n', sleep: float = 2.0, with_spinner=False, spinner_type: str = 'dot', to_file=True) -> None:
        orig_end = end
        if with_spinner:
            end = ' '

        sys.stdout.write(f'{start}{msg}{end}')
        sys.stdout.flush()

        if self.Conf.log_to_file \
        and to_file \
        and msg != self.prev_log_msg:
            logging.info(msg)
            self.prev_log_msg = msg

        if sleep > 0:
            if not with_spinner:
                time.sleep(sleep)
            else:
                spinner(sleep, type=spinner_type, end=orig_end)


    def print_head(self) -> None:
        w: int = 70

        self.log(f'---=|| D e s t i n y \'s  P a t h  4 ||=---'.ljust(w, '-'), end='\n\n', sleep=0, to_file=False)

        self.log(f'{self.Lang.stats_label_shell_name}: {self.Lang.stats_text_shell_name.format(shell_name=self.Save.shell_name)}', sleep=0, to_file=False)
        self.log(f'{self.Lang.stats_label_region}: {self.Lang.stats_text_region.format(region_level=int(self.Save.region_level), region_name=self.Save.region_name)}', sleep=0, to_file=False)
        self.log(f'{self.Lang.stats_label_hot_wallet}: {self.Lang.stats_text_wallet.format(currency_amount=ff(self.Save.hot_wallet), currency_name=self.Conf.currency_name)}', sleep=0, to_file=False)
        self.log(f'{self.Lang.stats_label_cold_wallet}: {self.Lang.stats_text_wallet.format(currency_amount=ff(self.Save.cold_wallet), currency_name=self.Conf.currency_name)}', sleep=0, to_file=False)
        self.log(f'{self.Lang.stats_label_wagon}: {self.Lang.stats_text_wagon.format(free_space_count=max(0, self.Conf.inventory_size - len(self.Save.inventory.keys())), inventory_size=self.Conf.inventory_size)}', sleep=0, to_file=False)

        if self.Save.total_distance_traveled > 0:
            self.log(f'{self.Lang.stats_label_total_distance_traveled}: {self.Lang.stats_text_total_distance_traveled.format(total_distance_traveled=ff(self.Save.total_distance_traveled, prec=3))}', start='\n', sleep=0, to_file=False)

        if self.Save.total_items_looted > 0:
            self.log(f'{self.Lang.stats_label_total_items_looted}: {self.Lang.stats_text_total_items_looted.format(total_items_looted=self.Save.total_items_looted, total_items_stolen_by_foes=self.Save.total_items_stolen_by_foes)}', sleep=0, to_file=False)

        if self.Save.total_items_sold > 0:
            self.log(f'{self.Lang.stats_label_total_items_sold}: {self.Lang.stats_text_total_items_sold.format(total_items_sold=self.Save.total_items_sold)}', sleep=0, to_file=False)

        if self.Save.total_trade_income > 0:
            self.log(f'{self.Lang.stats_label_total_trade_income}: {self.Lang.stats_text_total_trade_income.format(total_trade_income=ff(self.Save.total_trade_income), currency_name=self.Conf.currency_name, total_currency_stolen_by_hackers=ff(self.Save.total_currency_stolen_by_hackers))}', sleep=0, to_file=False)

        if self.Save.total_kills > 0:
            self.log(f'{self.Lang.stats_label_total_kills}: {self.Lang.stats_text_total_kills.format(total_kills=self.Save.total_kills)}', sleep=0, to_file=False)

        if self.Save.total_deaths > 0:
            self.log(f'{self.Lang.stats_label_total_deaths}: {self.Lang.stats_text_total_deaths.format(total_deaths=self.Save.total_deaths, total_deaths_by_foes=self.Save.total_deaths_by_foes, total_random_deaths=self.Save.total_random_deaths)}', sleep=0, to_file=False)

        log_file_size: str = f'({ff(self.Conf.log_file.stat().st_size / 1024 / 1024, prec=1)}m)' if self.cliargs.log_to_file and self.Conf.log_file.is_file() else ''

        self.log(f'---(i{self.game_loop_iter_count})---{log_file_size}---'.ljust(w, '-'), start='\n', end='\n\n', sleep=0, to_file=False)
