from .translation import TRANSLATION




class DP4_Lang:
    stats_label_shell_name: str
    stats_text_shell_name: str
    stats_label_hot_wallet: str
    stats_label_cold_wallet: str
    stats_text_wallet: str
    stats_label_wagon: str
    stats_text_wagon: str
    stats_label_total_distance_traveled: str
    stats_label_region: str
    stats_label_total_items_looted: str
    stats_label_total_items_stolen_by_foes: str
    stats_label_total_items_sold: str
    stats_label_total_trade_income: str
    stats_label_total_currency_stolen_by_hackers: str
    stats_label_total_kills: str
    stats_label_total_deaths: str
    stats_text_total_distance_traveled: str
    stats_text_region: str
    stats_text_total_items_looted: str
    stats_text_total_items_stolen_by_foes: str
    stats_text_total_items_sold: str
    stats_text_total_trade_income: str
    stats_text_total_currency_stolen_by_hackers: str
    stats_text_total_kills: str
    stats_text_total_deaths: str
    sim_wakeup: str
    sim_walk: str
    sim_walk_enternewregion: str
    sim_sell_wagonfull: str
    sim_sell_lookingforvendor: str
    sim_sell_foundshop: str
    sim_sell_negvendormod: str
    sim_sell_negvendormodresult: str
    sim_sell_solditem: str
    sim_sell_result: str
    sim_sell_leavingshop: str
    sim_transfer_currency_thresholdtriggered: str
    sim_transfer_currency_transfering: str
    sim_transfer_currency_result: str
    sim_death: str
    sim_rebirth_waiting: str
    sim_rebirth_calibrating: str
    sim_gift_strangerapproaches: str
    sim_gift_strangerwalksby: str
    sim_gift_yougetboxfromstranger: str
    sim_gift_youthankstranger: str
    sim_gift_strangernodsandwalksaway: str
    sim_gift_youopengift: str
    sim_hacker_hackersattacking: str
    sim_hacker_accessfailed: str
    sim_hacker_accessgained: str
    sim_hacker_walletwasempty: str
    sim_hacker_youlostcurrency: str
    sim_container_findcontainer: str
    sim_container_lookinside: str
    sim_entity_meet: str
    sim_entity_yourfirstreaction: str
    sim_entity_hostileentityreaction: str
    sim_entity_youflee: str
    sim_entity_bothattack: str
    sim_entity_friendlyentityreaction: str
    sim_entity_entityflee: str
    sim_entity_youattack: str
    sim_entity_entityactshostile: str
    sim_entity_friendlyyoureaction: str
    sim_entity_entityattack: str
    sim_entity_entityisopenforcontact: str
    sim_entity_entitydoesnotwantcontact: str
    sim_conversation_inprogress: str
    sim_conversation_entityapproves: str
    sim_conversation_getitem: str
    sim_conversation_youthankentity: str
    sim_conversation_entitylostinterest: str
    sim_conversation_end: str
    sim_fight_inprogress: str
    sim_fight_yougotkilled: str
    sim_fight_entitystealsitem: str
    sim_fight_youkilledentity: str
    sim_fight_yousearchcorpse: str
    sim_fight_youhidecorpse: str
    sim_find_loot_containerisempty: str
    sim_find_loot_finditem: str
    sim_find_loot_checkwagonspace: str
    sim_find_loot_discarditem: str
    sim_find_loot_storeitem: str


    def __init__(self, lang_code: str) -> None:
        for k, v in TRANSLATION[lang_code].items():
            setattr(self, k, v)
