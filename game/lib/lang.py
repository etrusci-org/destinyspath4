from .translation import L




class DP4_Lang:
    sim_wakeup: str = '[wakeup] You wake up in a shell named <{shell_name}>'
    sim_walk: str = '[walk] You walk the path'

    sim_sell_wagonfull: str = '[sell] The wagon is full'
    sim_sell_lookingforvendor: str = '[sell] Looking for a vendor'
    sim_sell_foundshop: str = '[sell] Found the shop of <{vendor_name}>'
    sim_sell_negvendormod: str = '[sell] Negotiating trade price modificator'
    sim_sell_negvendormodresult: str = '[sell] Negotiated {vendor_mod}'
    sim_sell_solditem: str = '[sell] Sold {item_count} [{item_name}] for {stack_value} {per_item_value}'
    sim_sell_result: str = '[sell] Earned {total_income} from {item_count} items'
    sim_sell_leavingshop: str = '[sell] Leaving the shop'

    sim_transfer_currency_thresholdtriggered: str = '[transfer_currency] Currency treshold triggered'
    sim_transfer_currency_transfering: str = '[transfer_currency] Transfering some {currency_name} to the cold wallet'
    sim_transfer_currency_result: str = '[transfer_currency] Secured {transfer_amount}'

    sim_death: str = '[death] You died because `{cause_of_death}´'

    sim_rebirth_waiting: str = '[rebirth] Waiting to be reborn'
    sim_rebirth_calibrating: str = '[rebirth] Calibrating reality'

    sim_gift_strangerapproaches: str = '[gift] A stranger is approaching'
    sim_gift_strangerwalksby: str = '[gift] He silently walks by'
    sim_gift_yougetboxfromstranger: str = '[gift] He puts a box in your hands'
    sim_gift_youthankstranger: str = '[gift] You thank the stranger'
    sim_gift_strangernodsandwalksaway: str = '[gift] The stranger nods and walks away'
    sim_gift_youopengift: str = '[gift] You open the box'

    sim_hacker_hackersattacking: str = '[hacker] Hackers are attacking your hot wallet'
    sim_hacker_accessfailed: str = '[hacker] They failed to gain access'
    sim_hacker_accessgained: str = '[hacker] They gained access'
    sim_hacker_walletwasempty: str = '[hacker] Luckily the hot wallet was empty'
    sim_hacker_youlostcurrency: str = '[hacker] You lost {stolen_amount}'

    sim_container_findcontainer: str = '[container] You stumble over |{container_name}|'
    sim_container_lookinside: str = '[container] Looking inside'

    sim_entity_meet: str = '[entity] You meet <{entity_name}>'
    sim_entity_yourfirstreaction: str = '[entity] You act {attitude_player}'
    sim_entity_hostileentityreaction: str = '[entity] <{entity_name}> taunts you'
    sim_entity_youflee: str = '[entity] You flee'
    sim_entity_bothattack: str = '[entity] You attack each other'
    sim_entity_friendlyentityreaction: str = '[entity] <{entity_name}> is trying to calm you down'
    sim_entity_entityflee: str = '[entity] <{entity_name}> is fleeing'
    sim_entity_youattack: str = '[entity] You attack <{entity_name}>'
    sim_entity_entityactshostile: str = '[entity] <{entity_name}> acts hostile'
    sim_entity_friendlyyoureaction: str = '[entity] You try to calm <{entity_name}> down'
    sim_entity_entityattack: str = '[entity] <{entity_name}> attacks you'
    sim_entity_entityisopenforcontact: str = '[entity] {entity_name} greets you'
    sim_entity_entitydoesnotwantcontact: str = '[entity] <{entity_name}> is in a hurry'

    sim_conversation_inprogress: str = '[conversation] Having a conversation about [{item_name}]'
    sim_conversation_entityapproves: str = '[conversation] <{entity_name}> is impressed by your knowledge'
    sim_conversation_getitem: str = '[conversation] You received [{item_name}] worth {item_value} as a gift'
    sim_conversation_youthankentity: str = '[conversation] You thank <{entity_name}>'
    sim_conversation_entitylostinterest: str = '[conversation] <{entity_name}> got bored and walks away'
    sim_conversation_end: str = '[conversation] Your paths diverge'

    sim_fight_inprogress: str = '[fight] Fighting hard and unfair'
    sim_fight_yougotkilled: str = '[fight] <{entity_name}> murdered you'
    sim_fight_entitystealsitem: str = '[fight] <{entity_name}> took {item_count} [{item_name}] worth {stack_value}'
    sim_fight_youkilledentity: str = '[fight] You murdered <{entity_name}>'
    sim_fight_yousearchcorpse: str = '[fight] Searching the corpse'
    sim_fight_youhidecorpse: str = '[fight] Hiding the corpse'

    sim_find_loot_containerisempty: str = '[find_loot] A dark void stares back at you'
    sim_find_loot_finditem: str = '[find_loot] Found [{item_name}]'
    sim_find_loot_checkwagonspace: str = '[find_loot] Looking for empty boxes on the wagon'
    sim_find_loot_discarditem: str = '[find_loot] Discarding [{item_name}]'
    sim_find_loot_storeitem: str = '[find_loot] Storing [{item_name}]'


    def __init__(self, lang_code: str, default_lang: str) -> None:
        if lang_code == default_lang:
            return

        for k, v in L[lang_code].items():
            setattr(self, k, v)
