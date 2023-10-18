import argparse
import pathlib
import random
import sys
import time

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
            help=f'path to the save data directory (default={self.Conf.save_dir})'
        )

        # self.CLIParser.add_argument('-L', '--lang',
        #     metavar='LANG_CODE',
        #     type=str,
        #     default=self.Conf.lang,
        #     choices=['de', 'en'],
        #     required=False,
        #     help=f'translation to use for output (default={self.Conf.lang})'
        # ) # commented-out until we have at least one translation

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
        lang_default = self.Conf.lang
        # self.Conf.lang = self.cliargs.lang # commented-out until we have at least one translation

        # init lang class
        self.Lang: DP4_Lang = DP4_Lang(lang_code=self.Conf.lang, default_lang=lang_default)

        # init save class
        self.Save = DP4_Save(file=self.Conf.save_file)



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



    def sim_wakeup(self) -> None:
        # self.log(f'[wakeup] You wake up in a shell named <{self.Save.shell_name}>', sleep=rffr(self.Conf.sim_wakeup_wakingup_duration), with_spinner=True)
        self.log(self.Lang.sim_wakeup.format(shell_name=self.Save.shell_name), sleep=rffr(self.Conf.sim_wakeup_wakingup_duration), with_spinner=True)


    def sim_walk(self) -> None:
        start = time.time()

        # self.log('[walk] You walk the path', sleep=rffr(self.Conf.sim_walk_walking_duration), with_spinner=True, spinner_type='arrow')
        self.log(self.Lang.sim_walk, sleep=rffr(self.Conf.sim_walk_walking_duration), with_spinner=True, spinner_type='arrow')

        self.update_distance_traveled(start)
        self.update_region_level()


    def sim_sell(self) -> None:
        # self.log('[sell] The wagon is full')
        self.log(self.Lang.sim_sell_wagonfull)
        # self.log('[sell] Looking for a vendor', sleep=rffr(self.Conf.sim_sell_searchvendor_duration), with_spinner=True)
        self.log(self.Lang.sim_sell_lookingforvendor, sleep=rffr(self.Conf.sim_sell_searchvendor_duration), with_spinner=True)

        vendor_name = self.String.random_name('entity')
        # self.log(f'[sell] Found the shop of <{vendor_name}>')
        self.log(self.Lang.sim_sell_foundshop.format(vendor_name=vendor_name))

        # self.log('[sell] Negotiating trade price modificator', sleep=rffr(self.Conf.sim_sell_negvendormod_duration), with_spinner=True)
        self.log(self.Lang.sim_sell_negvendormod, sleep=rffr(self.Conf.sim_sell_negvendormod_duration), with_spinner=True)

        vendor_mod = rffr(self.Conf.sim_sell_vendormod_range)
        # self.log(f'[sell] Negotiated {ff(vendor_mod)}')
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

            # self.log(f'[sell] Sold {item_count} [{item_name}] for {ff(stack_value)}{per_item_value_str}')
            self.log(self.Lang.sim_sell_solditem.format(item_count=item_count, item_name=item_name, stack_value=ff(stack_value), per_item_value=per_item_value_str))

        # self.log(f'[sell] Earned {ff(total_income)} from {total_items_sold} items')
        self.log(self.Lang.sim_sell_result.format(total_income=ff(total_income), item_count=total_items_sold))
        # self.log('[sell] Leaving the shop', sleep=rffr(self.Conf.sim_sell_leavevendor_duration), with_spinner=True)
        self.log(self.Lang.sim_sell_leavingshop, sleep=rffr(self.Conf.sim_sell_leavevendor_duration), with_spinner=True)


    def sim_transfer_currency(self) -> None:
        # self.log('[transfer_currency] Currency treshold triggered')
        self.log(self.Lang.sim_transfer_currency_thresholdtriggered)

        # self.log(f'[transfer_currency] Transfering some {self.Conf.currency_name} to the cold wallet', sleep=rffr(self.Conf.sim_transfer_currency_transfer_duration), with_spinner=True)
        self.log(self.Lang.sim_transfer_currency_transfering.format(currency_name=self.Conf.currency_name), sleep=rffr(self.Conf.sim_transfer_currency_transfer_duration), with_spinner=True)

        transfer_amount = self.Save.hot_wallet * self.Conf.sim_transfer_currency_transfer_amount_mod

        self.Save.cold_wallet += transfer_amount
        self.Save.hot_wallet -= transfer_amount

        # self.log(f'[transfer_currency] Secured {ff(transfer_amount)}')
        self.log(self.Lang.sim_transfer_currency_result.format(transfer_amount=ff(transfer_amount)))


    def sim_death(self) -> None:
        self.Save.total_deaths += 1
        self.Save.total_random_deaths += 1

        deathcause = self.String.random_name('deathcause')

        # self.log(f'[death] You died because `{deathcause}´', sleep=rffr(self.Conf.sim_death_dying_duration), with_spinner=True)
        self.log(self.Lang.sim_death.format(cause_of_death=deathcause), sleep=rffr(self.Conf.sim_death_dying_duration), with_spinner=True)

        self.sim_rebirth()


    def sim_rebirth(self) -> None:
        # self.log('[rebirth] Waiting to be reborn', sleep=rffr(self.Conf.sim_rebirth_waiting_duration), with_spinner=True)
        self.log(self.Lang.sim_rebirth_waiting, sleep=rffr(self.Conf.sim_rebirth_waiting_duration), with_spinner=True)

        self.Save.shell_name = self.String.random_name('entity')
        self.String.current_shell_name = self.Save.shell_name

        self.sim_wakeup()

        # self.log(f'[rebirth] Calibrating reality', sleep=rffr(self.Conf.sim_rebirth_calibrate_duration), with_spinner=True)
        self.log(self.Lang.sim_rebirth_calibrating, sleep=rffr(self.Conf.sim_rebirth_calibrate_duration), with_spinner=True)


    def sim_gift(self) -> None:
        # self.log('[gift] A stranger is approaching', sleep=rffr(self.Conf.sim_gift_approach_duration), with_spinner=True)
        self.log(self.Lang.sim_gift_strangerapproaches, sleep=rffr(self.Conf.sim_gift_approach_duration), with_spinner=True)

        if not self.Event.win:
            # self.log('[gift] He silently walks by')
            self.log(self.Lang.sim_gift_fail)
            return

        # self.log(f'[gift] He puts a box in your hands')
        self.log(self.Lang.sim_gift_yougetboxfromstranger)
        # self.log(f'[gift] You thank the stranger')
        self.log(self.Lang.sim_gift_youthankstranger)
        # self.log('[gift] The stranger nods and walks away')
        self.log(self.Lang.sim_gift_strangernodsandwalksaway)

        # self.log('[gift] You open the box', sleep=rffr(self.Conf.sim_gift_opengift_duration), with_spinner=True)
        self.log(self.Lang.sim_gift_youopengift, sleep=rffr(self.Conf.sim_gift_opengift_duration), with_spinner=True)

        self.sim_find_loot(count=1)


    def sim_hacker(self) -> None:
        self.log(self.Lang.sim_hacker_hackersattacking, sleep=rffr(self.Conf.sim_hacker_attack_duration), with_spinner=True)

        if self.Event.win:
            # self.log('[hacker] They failed to gain access')
            self.log(self.Lang.sim_hacker_accessfailed)
            return

        # self.log('[hacker] They gained access', sleep=rffr(self.Conf.sim_hacker_hacking_duration), with_spinner=True)
        self.log(self.Lang.sim_hacker_accessgained, sleep=rffr(self.Conf.sim_hacker_hacking_duration), with_spinner=True)

        if self.Save.hot_wallet == 0:
            # self.log('[hacker] Luckily the hot wallet was empty')
            self.log(self.Lang.sim_hacker_walletwasempty)
            return

        stolen_amount = self.Save.hot_wallet

        self.Save.hot_wallet -= stolen_amount

        self.Save.total_currency_stolen_by_hackers += stolen_amount

        # self.log(f'[hacker] You lost {ff(stolen_amount)}')
        self.log(self.Lang.sim_hacker_youlostcurrency.format(stolen_amount=ff(stolen_amount)))


    def sim_container(self) -> None:
        container_name = self.String.random_name('container')

        # self.log(f'[container] You stumble over |{container_name}|')
        self.log(self.Lang.sim_container_findcontainer.format(container_name=container_name))

        # self.log('[container] Looking inside', sleep=rffr(self.Conf.sim_container_checking_duration), with_spinner=True)
        self.log(self.Lang.sim_container_lookinside, sleep=rffr(self.Conf.sim_container_checking_duration), with_spinner=True)

        self.sim_find_loot()


    def sim_entity(self) -> None:
        entity_name = self.String.random_name('entity')

        # self.log(f'[entity] You meet <{entity_name}>')
        self.log(self.Lang.sim_entity_meet.format(entity_name=entity_name))

        attitude_player: str = random.choice(self.Conf.sim_entity_attitude)
        attitude_entity: str = random.choice(self.Conf.sim_entity_attitude)

        # self.log(f'[entity] You act {attitude_player}', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
        self.log(self.Lang.sim_entity_yourfirstreaction.format(attitude_player=attitude_player), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

        if attitude_player == 'hostile':

            if attitude_entity == 'hostile':
                # self.log(f'[entity] <{entity_name}> taunts you', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                self.log(self.Lang.sim_entity_hostileentityreaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    # self.log('[entity] You flee')
                    self.log(self.Lang.sim_entity_youflee)
                    return
                # self.log(f'[entity] You attack each other')
                self.log(self.Lang.sim_entity_bothattack)
                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                # self.log(f'[entity] <{entity_name}> is trying to calm you down', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                self.log(self.Lang.sim_entity_friendlyentityreaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                if random.random() < rffr(self.Conf.sim_entity_entityflee_chance_range):
                    # self.log(f'[entity] <{entity_name}> is fleeing')
                    self.log(self.Lang.sim_entity_entityflee.format(entity_name=entity_name))
                    return
                # self.log(f'[entity] You attack <{entity_name}>')
                self.log(self.Lang.sim_entity_youattack.format(entity_name=entity_name))
                self.sim_fight(entity_name)

        if attitude_player == 'friendly':

            if attitude_entity == 'hostile':
                # self.log(f'[entity] <{entity_name}> acts hostile', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                self.log(self.Lang.sim_entity_entityactshostile.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

                # self.log(f'[entity] You try to calm <{entity_name}> down', sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)
                self.log(self.Lang.sim_entity_friendlyyoureaction.format(entity_name=entity_name), sleep=rffr(self.Conf.sim_entity_acting_duration), with_spinner=True)

                if random.random() < rffr(self.Conf.sim_entity_playerflee_chance_range):
                    # self.log('[entity] You flee')
                    self.log(self.Lang.sim_entity_youflee)
                    return

                # self.log(f'[entity] <{entity_name}> attacks you')
                self.log(self.Lang.sim_entity_entityattack.format(entity_name=entity_name))

                self.sim_fight(entity_name)

            if attitude_entity == 'friendly':
                if random.random() < rffr(self.Conf.sim_entity_conversation_chance_range):
                    # self.log(f'[entity] {entity_name} greets you')
                    self.log(self.Lang.sim_entity_entityisopenforcontact)
                    self.sim_conversation(entity_name)
                    return

                # self.log(f'[entity] <{entity_name}> is in a hurry')
                self.log(self.Lang.sim_entity_entitydoesnotwantcontact)


    def sim_conversation(self, entity_name: str) -> None:
        item_name = self.String.random_name('object')

        # self.log(f'[conversation] Having a conversation about [{item_name}]', sleep=rffr(self.Conf.sim_conversation_convo_duration), with_spinner=True)
        self.log(self.Lang.sim_conversation_inprogress.format(item_name=item_name), sleep=rffr(self.Conf.sim_conversation_convo_duration), with_spinner=True)

        if self.Event.win:
            # self.log(f'[conversation] <{entity_name}> is impressed by your knowledge')
            self.log(self.Lang.sim_conversation_entityapproves.format(entity_name=entity_name))

            self.add_inventory_item(item_name)

            # self.log(f'[conversation] You received [{item_name}] worth {ff(self.Save.inventory[item_name]["item_value"])} as a gift')
            self.log(self.Lang.sim_conversation_getitem.format(item_name=item_name, item_value=ff(self.Save.inventory[item_name]['item_value'])))
            # self.log(f'[conversation] You thank <{entity_name}>')
            self.log(self.Lang.sim_conversation_youthankentity.format(entity_name=entity_name))
        else:
            # self.log(f'[conversation] <{entity_name}> got bored')
            self.log(self.Lang.sim_conversation_entitylostinterest.format(entity_name=entity_name))

        # self.log('[conversation] Your paths diverge')
        self.log(self.Lang.sim_conversation_end)


    def sim_fight(self, entity_name: str) -> None:
        # self.log(f'[fight] Fighting', sleep=rffr(self.Conf.sim_fight_fighting_duration), with_spinner=True)
        self.log(self.Lang.sim_fight_inprogress, sleep=rffr(self.Conf.sim_fight_fighting_duration), with_spinner=True)

        if not self.Event.win:
            self.Save.total_deaths += 1
            self.Save.total_deaths_by_foes += 1

            # self.log(f'[fight] <{entity_name}> murdered you')
            self.log(self.Lang.sim_fight_yougotkilled.format(entity_name=entity_name))

            if len(self.Save.inventory.keys()) > 0:
                stolen_items_count: int = random.randint(self.Conf.sim_fight_stolenitemsmin_count, max(1, int(len(self.Save.inventory.keys()) * self.Conf.sim_fight_stolenitemsmax_mod)))
                stolen_items: list = random.sample(sorted(self.Save.inventory), stolen_items_count)
                for item_name in stolen_items:
                    item_count = self.Save.inventory[item_name]['count']
                    stack_value = self.Save.inventory[item_name]['stack_value']

                    self.Save.total_items_stolen_by_foes += item_count

                    del self.Save.inventory[item_name]

                    # self.log(f'[fight] <{entity_name}> took {item_count} [{item_name}] worth {ff(stack_value)}')
                    self.log(self.Lang.sim_fight_entitystealsitem.format(entity_name=entity_name, item_count=item_count, item_name=item_name, stack_value=ff(stack_value)))

            self.sim_rebirth()
            return

        self.Save.total_kills += 1

        # self.log(f'[fight] You murdered <{entity_name}>')
        self.log(self.Lang.sim_fight_youkilledentity.format(entity_name=entity_name))

        # self.log(f'[fight] Searching the corpse', sleep=rffr(self.Conf.sim_fight_searchcorpse_duration), with_spinner=True)
        self.log(self.Lang.sim_fight_yousearchcorpse, sleep=rffr(self.Conf.sim_fight_searchcorpse_duration), with_spinner=True)

        self.sim_find_loot()

        # self.log(f'[fight] Hiding the corpse', sleep=rffr(self.Conf.sim_fight_hidecorpse_duration), with_spinner=True)
        self.log(self.Lang.sim_fight_youhidecorpse, sleep=rffr(self.Conf.sim_fight_hidecorpse_duration), with_spinner=True)


    def sim_find_loot(self, count: int = None) -> None:
        item_count: int = count if count else random.randint(*self.Conf.sim_find_loot_count)

        if item_count == 0:
            # self.log(f'[find_loot] A dark void stares back at you')
            self.log(self.Lang.sim_find_loot_containerisempty)
            return

        found_items: list[str] = []

        while len(found_items) < item_count:
            item_name: str = self.String.random_name('object')
            if item_name in found_items:
                continue
            found_items.append(item_name)
            # self.log(f'[find_loot] Found [{item_name}]')
            self.log(self.Lang.sim_find_loot_finditem.format(item_name=item_name))

        # self.log(f'[find_loot] Looking for empty boxes on the wagon', sleep=rffr(self.Conf.sim_find_loot_wagoncheck_duration), with_spinner=True)
        self.log(self.Lang.sim_find_loot_checkwagonspace, sleep=rffr(self.Conf.sim_find_loot_wagoncheck_duration), with_spinner=True)

        for item_name in found_items:
            if len(self.Save.inventory.keys()) >= self.Conf.inventory_size and not self.Save.inventory.get(item_name):
                # self.log(f'[find_loot] Discarding [{item_name}]')
                self.log(self.Lang.sim_find_loot_discarditem.format(item_name=item_name))
                continue
            # self.log(f'[find_loot] Storing [{item_name}]')
            self.log(self.Lang.sim_find_loot_storeitem.format(item_name=item_name))
            self.add_inventory_item(item_name)



    # -----------------------------------------------------------------------



    def update_distance_traveled(self, started_walking_on: float) -> None:
        self.Save.total_distance_traveled += self.Conf.travel_speed * ((time.time() - started_walking_on) / 3_600)


    def update_region_level(self) -> None:
        self.Save.region_level = ((((8 * (self.Save.total_distance_traveled * 100) / 100 + 1) ** 0.5) - 1) / 2) + 1



    # -----------------------------------------------------------------------



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


    def print_head(self) -> None:
        w: int = 60

        self.log(f'~~~-=[ D e s t i n y \' s   P a t h   4 ]=-~~~'.ljust(w, '~'), end='\n\n', sleep=0)

        self.log(f'       current shell: {self.Save.shell_name}', sleep=0)
        self.log(f'          hot wallet: {ff(self.Save.hot_wallet)} {self.Conf.currency_name}', sleep=0)
        self.log(f'         cold wallet: {ff(self.Save.cold_wallet)} {self.Conf.currency_name}', sleep=0)
        self.log(f'               wagon: {max(0, self.Conf.inventory_size - len(self.Save.inventory.keys()))} empty boxes', end='\n', sleep=0)

        if self.Save.total_distance_traveled > 0:
            self.log(f'   distance traveled: {ff(self.Save.total_distance_traveled, prec=3)} km', start='\n', sleep=0)

        if self.Save.region_level > 1:
            self.log(f'        region level: {ff(self.Save.region_level, prec=3)}', sleep=0)

        if self.Save.total_items_looted > 0:
            self.log(f'        items looted: {self.Save.total_items_looted}', sleep=0)

        if self.Save.total_items_stolen_by_foes > 0:
            self.log(f'items stolen by foes: {self.Save.total_items_stolen_by_foes}', sleep=0)

        if self.Save.total_items_sold > 0:
            self.log(f'          items sold: {self.Save.total_items_sold}', sleep=0)

        if self.Save.total_trade_income > 0:
            self.log(f'        trade income: {ff(self.Save.total_trade_income)} {self.Conf.currency_name}', sleep=0)

        if self.Save.total_currency_stolen_by_hackers > 0:
            self.log(f'   stolen by hackers: {ff(self.Save.total_currency_stolen_by_hackers)} {self.Conf.currency_name}', sleep=0)

        if self.Save.total_kills > 0:
            self.log(f'               kills: {self.Save.total_kills}', sleep=0)

        if self.Save.total_deaths > 0:
            self.log(f'              deaths: {self.Save.total_deaths}', sleep=0)

        if self.Save.total_deaths_by_foes > 0:
            self.log(f'      deaths by foes: {self.Save.total_deaths_by_foes}', sleep=0)

        if self.Save.total_random_deaths > 0:
            self.log(f'  deaths by accident: {self.Save.total_random_deaths}', sleep=0)

        self.log(f'~~~=[ {self.Conf.save_name} ]'.rjust(w, '~'), start='\n', end='\n\n\n', sleep=0)
