'''
Formatting rules:
    region -> as is
    container -> |container_name|
    object/item -> [item_name]
    entity -> <entity_name>
    randomdeath -> `cause_of_death´
'''


TRANSLATION: dict[str, dict[str, str]] = {}


# en - english (default)
TRANSLATION['en'] = {
    'stats_label_shell_name': '               shell',
    'stats_text_shell_name': '{shell_name}',

    'stats_label_hot_wallet': '          hot wallet',
    'stats_label_cold_wallet': '         cold wallet',
    'stats_text_wallet': '{currency_amount} {currency_name}',

    'stats_label_wagon': '               wagon',
    'stats_text_wagon': '{free_space_count} / {inventory_size} free boxes',

    'stats_label_total_distance_traveled': '   distance traveled',
    'stats_text_total_distance_traveled': '{total_distance_traveled} km',

    'stats_label_region': '              region',
    'stats_text_region': '{region_name} (level:{region_level})',

    'stats_label_total_items_looted': '         items found',
    'stats_text_total_items_looted': '{total_items_looted} (lost:{total_items_stolen_by_foes})',

    'stats_label_total_items_sold': '          items sold',
    'stats_text_total_items_sold': '{total_items_sold}',

    'stats_label_total_trade_income': '              income',
    'stats_text_total_trade_income': '{total_trade_income} {currency_name} (lost:{total_currency_stolen_by_hackers})',

    'stats_label_total_kills': '               kills',
    'stats_text_total_kills': '{total_kills}',

    'stats_label_total_deaths': '              deaths',
    'stats_text_total_deaths': '{total_deaths} (fight:{total_deaths_by_foes} random:{total_random_deaths})',

    'sim_wakeup': 'Waking up in a shell named <{shell_name}>',

    'sim_walk': 'Walking the path',
    'sim_walk_enternewregion': 'Entering region {region_name} (level:{region_level})',

    'sim_sell_wagonfull': 'The wagon is full',
    'sim_sell_lookingforvendor': 'Looking for a merchant',
    'sim_sell_foundshop': 'Found the shop of <{vendor_name}>',
    'sim_sell_negvendormod': 'Negotiating trade price modificator',
    'sim_sell_negvendormodresult': 'Negotiated {vendor_mod}',
    'sim_sell_solditem': 'Selling {item_count} [{item_name}] for {stack_value} {currency_name} {per_item_value}',
    'sim_sell_result': 'Earned {total_income} {currency_name} from {item_count} items',
    'sim_sell_leavingshop': 'Leaving the shop',

    'sim_transfer_currency_thresholdtriggered': 'Currency transfer treshold triggered',
    'sim_transfer_currency_transfering': 'Transfering some {currency_name} to the cold wallet',
    'sim_transfer_currency_result': 'Secured {transfer_amount} {currency_name}',

    'sim_death': 'Died because `{cause_of_death}´',

    'sim_rebirth_waiting': 'Waiting to be reborn',
    'sim_rebirth_calibrating': 'Calibrating new reality',

    'sim_gift_strangerapproaches': 'A stranger is approaching',
    'sim_gift_strangerwalksby': 'He silently walks by',
    'sim_gift_yougetboxfromstranger': 'He puts a box in your hands',
    'sim_gift_youthankstranger': 'You thank the stranger',
    'sim_gift_strangernodsandwalksaway': 'The stranger nods and walks away',
    'sim_gift_youopengift': 'Opening the box',

    'sim_hacker_hackersattacking': 'Hackers are attacking',
    'sim_hacker_accessfailed': 'They failed to gain access',
    'sim_hacker_accessgained': 'They gained access',
    'sim_hacker_walletwasempty': 'Luckily the hot wallet was empty',
    'sim_hacker_youlostcurrency': '{stolen_amount} {currency_name} were stolen',

    'sim_container_findcontainer': 'You stumble over |{container_name}|',
    'sim_container_lookinside': 'Looking inside',

    'sim_entity_meet': 'Meeting <{entity_name}>',
    'sim_entity_yourfirstreaction': 'Acting {attitude_player}',
    'sim_entity_hostileentityreaction': '<{entity_name}> taunts you',
    'sim_entity_youflee': 'Fleeing',
    'sim_entity_bothattack': 'Attacking each other',
    'sim_entity_friendlyentityreaction': '<{entity_name}> is trying to calm you down',
    'sim_entity_entityflee': '<{entity_name}> flees',
    'sim_entity_youattack': 'Attacking <{entity_name}>',
    'sim_entity_entityactshostile': '<{entity_name}> acts hostile',
    'sim_entity_friendlyyoureaction': 'Trying to calm <{entity_name}> down',
    'sim_entity_entityattack': '<{entity_name}> attacks',
    'sim_entity_entityisopenforcontact': '<{entity_name}> greets',
    'sim_entity_entitydoesnotwantcontact': '<{entity_name}> is in a hurry',

    'sim_conversation_inprogress': 'Having a conversation about [{item_name}]',
    'sim_conversation_entityapproves': '<{entity_name}> must now go',
    'sim_conversation_getitem': 'You received [{item_name}] worth {item_value} as a gift',
    'sim_conversation_youthankentity': 'You thank <{entity_name}>',
    'sim_conversation_entitylostinterest': '<{entity_name}> got bored and walks away',
    'sim_conversation_end': 'Your paths diverge',

    'sim_fight_inprogress': 'Fighting',
    'sim_fight_yougotkilled': '<{entity_name}> murdered you',
    'sim_fight_entitystealsitem': '<{entity_name}> stole {item_count} [{item_name}]',
    'sim_fight_youkilledentity': 'Murdered <{entity_name}>',
    'sim_fight_yousearchcorpse': 'Searching the corpse',
    'sim_fight_youhidecorpse': 'Hiding the corpse',

    'sim_find_loot_containerisempty': 'Found nothing',
    'sim_find_loot_finditem': 'Found [{item_name}]',
    'sim_find_loot_checkwagonspace': 'Checking the storage boxes on your wagon',
    'sim_find_loot_discarditem': 'Discarding [{item_name}]',
    'sim_find_loot_storeitem': 'Storing [{item_name}]',
}


# de - german
# TRANSLATION['de'] = TRANSLATION['en'] | {
#     # TODO :-)
# }


# xy - your language example
# will inherit everything from 'en'
# to enable the translation, add 'de' to DP4_conf.lang_list
# TRANSLATION['xy'] = TRANSLATION['en'] | {
#     'sim_wakeup': 'hello i am {shell_name}',
#     'sim_walk': 'i walk',
# }
