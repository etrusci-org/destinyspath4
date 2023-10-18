import argparse
import pathlib
import random
import sys
import time

from lib.conf import DP4_Conf
from lib.event import DP4_Event
from lib.string import DP4_String
from lib.save import DP4_Save
from lib.terminal import clear_terminal
from lib.terminal import disable_terminal_cursor
from lib.terminal import enable_terminal_cursor
from lib.spinner import spinner
from lib.number import rffr
from lib.number import ff




class DP4_Core:
    def __init__(self) -> None:
        # init default conf
        # some stuff will be overriden below
        self.Conf: DP4_Conf = DP4_Conf()

        # init event class
        self.Event: DP4_Event = DP4_Event(event_group_chance=self.Conf.event_group_chance)

        # init string class
        self.String: DP4_String = DP4_String(asset_dir=self.Conf.asset_dir, load_from=self.Conf.string_load_from, string_part_chance=self.Conf.string_part_chance)

        # init cli parser
        self.CLIParser: argparse.ArgumentParser = argparse.ArgumentParser()

        self.CLIParser.add_argument('-p', '--play',
            action='store_true',
            help='play the game'
        )

        self.CLIParser.add_argument('-n', '--save-name',
            metavar='NAME',
            type=str,
            default=self.Conf.save_name,
            required=False,
            help=f'name of the save game to create or resume from (default={self.Conf.save_name})'
        )

        self.CLIParser.add_argument('-d', '--save-dir',
            metavar='PATH',
            type=str,
            default=self.Conf.save_dir,
            required=False,
            help=f'path to the save data directory, default={self.Conf.save_dir}'
        )

        # parse cli args
        self.cliargs: argparse.Namespace = self.CLIParser.parse_args()

        # check save dir from cli args and die hard if bad path
        save_dir: pathlib.Path = pathlib.Path(self.cliargs.save_dir).resolve()
        if not save_dir.exists() or not save_dir.is_dir():
            print(f'--save-dir does not exist or is not a directory: {save_dir}')
            exit(1)

        # all peaches and cream if we reach this line
        self.Conf.save_dir = save_dir
        self.Conf.save_file = self.Conf.save_dir.joinpath(f'{self.cliargs.save_name}.json')

        # init save class
        self.Save = DP4_Save(file=self.Conf.save_file)

        # test test test

        # print(self.cliargs)
        # print('Conf.game_dir', self.Conf.game_dir)
        # print('Conf.asset_dir', self.Conf.asset_dir)
        # print('Conf.save_dir', self.Conf.save_dir)
        # print('Conf.save_name', self.Conf.save_name)
        # print('Conf.save_file', self.Conf.save_file)
        # print('Save.file', self.Save.file)
        # print('Save.shell_name', self.Save.shell_name)
        # print('String.current_shell_name', self.String.current_shell_name)

        # self.Save.load(file=self.Conf.save_file)
        # self.add_inventory_item('foo')
        # self.add_inventory_item('bar')
        # self.Save.store(file=self.Conf.save_file)

        # print(self.String.random_name('object'))

        # print(self.item_value('foo'))
        # print(self.item_value('bar'))
        # print(self.item_value('foo bar'))
        # print(self.item_value('foo bar mo cow'))

        # print(random.randint(1, max(1, 0.5)))

        # exit(0)



    # -----------------------------------------------------------------------



    def play(self) -> None:
        clear_terminal()
        disable_terminal_cursor()

        self.Save.load()

        if self.Save.first_played == 0:
            self.Save.first_played = time.time()

        if not self.Save.shell_name:
            self.Save.shell_name = self.String.random_name('entity')

        self.String.current_shell_name = self.Save.shell_name # set current shell name in string class to avoid having the same name after a restart/rebirth

        try:
            self.game_loop()
        except KeyboardInterrupt:
            exit(0)
        finally:
            self.Save.store()
            self.log('Progress saved', start='\n', sleep=0)
            enable_terminal_cursor()


    def game_loop(self) -> None:
        is_first_iter = True

        while True:
            clear_terminal()

            self.print_head()

            self.simulate_event(is_first_iter)

            if not is_first_iter and time.time() - self.Save.last_saved > self.Conf.autosave_interval:
                self.Save.store()

            is_first_iter = False

            spinner(3, type='binary', start='\n')


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



    def sim_sell(self) -> None:
        self.log('[sell] The wagon is full')
        self.log('[sell] Looking for a vendor', sleep=rffr(self.Conf.sim_sell_searchvendor_duration), with_spinner=True)

        vendor_name = self.String.random_name('entity')
        self.log(f'[sell] Found the shop of <{vendor_name}>')

        self.log('[sell] Negotiating trade price modificator', sleep=rffr(self.Conf.sim_sell_negvendormod_duration), with_spinner=True)

        vendor_mod = rffr(self.Conf.sim_sell_vendormod_range)
        self.log(f'[sell] Negotiated {ff(vendor_mod)}')

        total_income: float = 0.0
        total_items_sold: int = 0

        for item_name in sorted(self.Save.inventory):
            item_count = self.Save.inventory[item_name]['count']
            item_value = self.Save.inventory[item_name]['item_value']
            stack_value = self.Save.inventory[item_name]['stack_value']

            total_income += stack_value
            total_items_sold += item_count

            self.Save.hot_wallet += stack_value

            self.Save.total_items_sold += item_count
            self.Save.total_trade_income += stack_value

            del self.Save.inventory[item_name]

            per_item_value_str = f' ({ff(item_value)}/item)' if item_count > 1 else ''
            self.log(f'[sell] Sold {item_count} [{item_name}] for {ff(stack_value)}{per_item_value_str}')

        self.log(f'[sell] Earned {ff(total_income)} from {total_items_sold} items')
        self.log('[sell] Leaving the shop', sleep=rffr(self.Conf.sim_sell_leavevendor_duration), with_spinner=True)


    def sim_transfer_currency(self) -> None:
        self.log('[transfer_currency] Currency treshold triggered')

        self.log(f'[transfer_currency] Transfering some {self.Conf.currency_name} to the cold wallet', sleep=rffr(self.Conf.sim_transfer_currency_transfer_duration), with_spinner=True)

        transfer_amount = self.Save.hot_wallet * self.Conf.sim_transfer_currency_transfer_amount_mod

        self.Save.cold_wallet += transfer_amount
        self.Save.hot_wallet -= transfer_amount

        self.log(f'[transfer_currency] Secured {transfer_amount} {self.Conf.currency_name}')


    def sim_wakeup(self) -> None:
        self.log(f'[wakeup] You wake up in a shell named <{self.Save.shell_name}>', sleep=rffr(self.Conf.sim_wakeup_wakingup_duration), with_spinner=True)


    def sim_walk(self) -> None:
        start = time.time()

        self.log('[walk] You walk the path', sleep=rffr(self.Conf.sim_walk_walking_duration), with_spinner=True, spinner_type='arrow')

        self.Save.total_distance_traveled += self.Conf.walking_speed * ((time.time() - start) / 3_600)


    def sim_death(self) -> None:
        self.Save.total_deaths += 1
        self.Save.total_random_deaths += 1

        deathcause = self.String.random_name('deathcause')
        self.log(f'[death] You died because *{deathcause}*', sleep=rffr(self.Conf.sim_death_dying_duration), with_spinner=True)
        self.sim_rebirth()


    def sim_rebirth(self) -> None:
        self.log('[rebirth] Waiting to be reborn', sleep=rffr(self.Conf.sim_rebirth_waiting_duration), with_spinner=True)

        self.Save.shell_name = self.String.random_name('entity')
        self.String.current_shell_name = self.Save.shell_name

        self.sim_wakeup()

        self.log(f'[rebirth] Calibrating reality', sleep=rffr(self.Conf.sim_rebirth_calibrate_duration), with_spinner=True)


    def sim_gift(self) -> None:
        self.log('[gift] A stranger is approaching', sleep=rffr(self.Conf.sim_gift_approach_duration), with_spinner=True)

        if not self.Event.win:
            self.log('[gift] He silently walks by')
            return

        self.log(f'[gift] He puts a box in your hands')
        self.log(f'[gift] You thank the stranger')
        self.log('[gift] The stranger nods and walks away')

        self.log('[gift] You open the box', sleep=rffr(self.Conf.sim_gift_opengift_duration), with_spinner=True)

        self.sim_find_loot(count=1)


    def sim_hacker(self) -> None:
        self.log('[hacker] Hackers are attacking your hot wallet', sleep=rffr(self.Conf.sim_hacker_attack_duration), with_spinner=True)

        if self.Event.win:
            self.log('[hacker] They failed to gain access')
        else:
            self.log('[hacker] They gained access', sleep=rffr(self.Conf.sim_hacker_hacking_duration), with_spinner=True)

            stolen_amount = self.Save.hot_wallet

            self.Save.hot_wallet -= stolen_amount

            self.Save.total_currency_stolen_by_hackers += stolen_amount

            if stolen_amount == 0:
                self.log('[hacker] Luckily the hot wallet was empty')
                return

            self.log(f'[hacker] You lost {stolen_amount} {self.Conf.currency_name}')


    def sim_container(self) -> None:
        container_name = self.String.random_name('container')

        self.log(f'[container] You stumble over |{container_name}|')

        self.log('[container] Looking inside', sleep=rffr(self.Conf.sim_container_checking_duration), with_spinner=True)

        self.sim_find_loot()


    def sim_entity(self) -> None:
        entity_name = self.String.random_name('entity')

        self.log(f'[entity] You meet <{entity_name}>')

        attitude_player: str = random.choice(self.Conf.sim_entity_attitude)
        attitude_entity: str = random.choice(self.Conf.sim_entity_attitude)
        # attitude_player: str = 'hostile'
        # attitude_entity: str = 'hostile'


        self.log(f'[entity] You act {attitude_player}', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

        if attitude_player == 'hostile':

            if attitude_entity == 'hostile':
                self.log(f'[entity] <{entity_name}> taunts you', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    self.log('[entity] You flee')
                    return
                self.log(f'[entity] You attack each other')
                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                self.log(f'[entity] <{entity_name}> is trying to calm you down', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_entityflee_chance_range):
                    self.log(f'<{entity_name}> is fleeing')
                    return
                self.log(f'[entity] You attack <{entity_name}>')
                self.sim_fight(entity_name)

        if attitude_player == 'friendly':

            if attitude_entity == 'hostile':
                self.log(f'[entity] <{entity_name}> taunts you', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    self.log('[entity] You flee')
                    return

                self.log('[entity] You could not care less')

                self.log(f'[entity] <{entity_name}> attacks you')
                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                if random.random() < rffr(self.Conf.sim_entity_conversation_chance_range):
                    self.log(f'[entity] {entity_name} greets you')
                    self.sim_conversation(entity_name)
                    return

                self.log(f'[entity] <{entity_name}> is in a hurry')


    def sim_conversation(self, entity_name: str) -> None:
        item_name = self.String.random_name('object')

        self.log(f'[conversation] Having a conversation about [{item_name}]', sleep=rffr(self.Conf.sim_conversation_convo_duration), with_spinner=True)

        if self.Event.win:
            self.log(f'[conversation] <{entity_name}> is impressed by your knowledge')
            self.add_inventory_item(item_name)
            self.log(f'[conversation] You received [{item_name}] as a gift')
        else:
            self.log(f'[conversation] <{entity_name}> got bored')

        self.log('[conversation] Your paths diverge')


    def sim_fight(self, entity_name: str) -> None:
        self.log(f'[fight] Fighting', sleep=rffr(self.Conf.sim_fight_fighting_duration), with_spinner=True)

        if not self.Event.win:
            self.Save.total_deaths += 1
            self.Save.total_deaths_by_foes += 1

            self.log(f'[fight] <{entity_name}> murdered you')

            if len(self.Save.inventory.keys()) > 0:
                stolen_items = random.sample(sorted(self.Save.inventory), random.randint(1, max(1, int(len(self.Save.inventory.keys()) / 2))))
                for item_name in stolen_items:
                    item_count = self.Save.inventory[item_name]['count']
                    stack_value = self.Save.inventory[item_name]['stack_value']

                    self.Save.total_items_stolen_by_foes += item_count

                    del self.Save.inventory[item_name]

                    self.log(f'[fight] <{entity_name}> took {item_count} [{item_name}] worth {stack_value} {self.Conf.currency_name}')

            self.sim_rebirth()
            return

        self.Save.total_kills += 1

        self.log(f'[fight] You murdered <{entity_name}>')

        self.log(f'[fight] Searching the corpse', sleep=rffr(self.Conf.sim_fight_searchcorpse_duration), with_spinner=True)

        self.sim_find_loot()

        self.log(f'[fight] Hiding the corpse', sleep=rffr(self.Conf.sim_fight_hidecorpse_duration), with_spinner=True)


    def sim_find_loot(self, count: int = None) -> None:
        item_count: int = count if count else random.randint(*self.Conf.sim_find_loot_count)

        if item_count < 1:
            self.log(f'[find_loot] There is nothing inside')
            return

        found_items: list[str] = []

        while len(found_items) < item_count:
            item_name: str = self.String.random_name('object')
            if item_name in found_items:
                continue
            found_items.append(item_name)
            self.log(f'[find_loot] Found [{item_name}]')

        self.log(f'[find_loot] Looking for free boxes on the wagon', sleep=rffr(self.Conf.sim_find_loot_wagoncheck_duration), with_spinner=True)

        for item_name in found_items:
            if self.Conf.inventory_size - len(self.Save.inventory.keys()) > 0:
                self.log(f'[find_loot] Storing [{item_name}]')
                self.add_inventory_item(item_name)
            else:
                if not self.Save.inventory.get(item_name):
                    self.log(f'[find_loot] Discarding [{item_name}]')
                else:
                    self.log(f'[find_loot] Storing [{item_name}]')
                    self.add_inventory_item(item_name)



    # -----------------------------------------------------------------------



    def add_inventory_item(self, item_name: str):
        self.Save.total_items_looted += 1

        if not self.Save.inventory.get(item_name):
            item_value = self.item_value(item_name)
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



    def log(self, msg: str = '', start: str = '', end: str = '\n', sleep: float = 1.5, with_spinner=False, spinner_type: str = 'dot') -> None:
        orig_end = end
        if with_spinner:
            end = ' '

        sys.stdout.write(f'{start}{msg}{end}')
        sys.stdout.flush()

        if sleep > 0:
            if not with_spinner:
                time.sleep(sleep)
            else:
                spinner(sleep, type=spinner_type, end=orig_end)


    def print_head(self):
        w: int = 60

        self.log('~~~ D E S T I N Y \' S ~ P A T H ~ 4 ~~~'.ljust(w, '~'), end='\n\n', sleep=0)

        self.log(f'current shell: {self.Save.shell_name}', sleep=0)
        self.log(f'   hot wallet: {ff(self.Save.hot_wallet)} {self.Conf.currency_name}', sleep=0)
        self.log(f'  cold wallet: {ff(self.Save.cold_wallet)} {self.Conf.currency_name}', sleep=0)
        self.log(f'        wagon: {max(0, self.Conf.inventory_size - len(self.Save.inventory.keys()))} empty boxes', end='\n\n', sleep=0)

        self.log(f'         distance traveled: {ff(self.Save.total_distance_traveled, prec=3)} km', sleep=0)

        if self.Save.total_items_looted > 0:
            self.log(f'              items looted: {self.Save.total_items_looted}', sleep=0)

        if self.Save.total_items_sold > 0:
            self.log(f'                items sold: {self.Save.total_items_sold}', sleep=0)

        if self.Save.total_trade_income > 0:
            self.log(f'              trade income: {ff(self.Save.total_trade_income)} {self.Conf.currency_name}', sleep=0)

        if self.Save.total_currency_stolen_by_hackers > 0:
            self.log(f'currency stolen by hackers: {ff(self.Save.total_currency_stolen_by_hackers)} {self.Conf.currency_name}', sleep=0)

        if self.Save.total_items_stolen_by_foes > 0:
            self.log(f'      items stolen by foes: {self.Save.total_items_stolen_by_foes}', sleep=0)

        if self.Save.total_kills > 0:
            self.log(f'                     kills: {self.Save.total_kills}', sleep=0)

        if self.Save.total_deaths > 0:
            self.log(f'                    deaths: {self.Save.total_deaths}', sleep=0)

        if self.Save.total_deaths_by_foes > 0:
            self.log(f'            deaths by foes: {self.Save.total_deaths_by_foes}', sleep=0)

        if self.Save.total_random_deaths > 0:
            self.log(f'        deaths by accident: {self.Save.total_random_deaths}', sleep=0)

        self.log(f'~'.rjust(w, '~'), start='\n', end='\n\n', sleep=0)
