import pathlib




class DP4_Conf:
    # game root directory
    game_dir: pathlib.Path = pathlib.Path(__file__).parents[1].resolve()

    # assets directory with string files and stuff
    asset_dir: pathlib.Path = game_dir.joinpath('asset')

    # directory for save files
    # can be overriden with cliargs
    save_dir: pathlib.Path = game_dir.joinpath('save')

    # save file name without extension
    # can be overriden with cliargs
    save_name: str = 'save1'

    # save file path
    # is set in DP4_Core.__init__
    save_file: pathlib.Path

    # the default language code of the default DP4_Lang translation
    # see DP4_Lang.__init__
    # see translation.py
    lang: str = 'en'

    # language codes to make available
    lang_list: list[str] = [
        'en',
        # 'de',
        # 'xy',
    ]

    # auto-save interval in seconds
    # the game will always try to save on exit
    autosave_interval: int = 180

    # chances for event groups to be triggered (after DP4_Core.sim_walk)
    # order from lowest to higest chance
    # let the last one be 1.0 (default)
    # see DP4_Event.new
    # valid range: 0.0 - 1.0
    event_group_chance: dict[str, float] = {
        'death': 0.017,
        'gift': 0.033,
        'hacker': 0.041,
        'container': 0.211,
        'entity': 1.0,
    }

    # chances of name parts to be added
    # see DP4_String.random_name
    # valid range: 0.0 - 1.0
    string_part_chance: dict[str, float] = {
        'container_prefix': 0.35,
        'container_suffix': 0.25,
        'object_prefix': 0.31,
        'object_suffix': 0.13,
        'entity_prefix': 0.21,
        'entity_suffix': 0.11,
    }

    # filenames without extensions to load the string data from
    # the file extension is expected to be .dat
    # see game/asset/ directory
    # see DP4_String.__init__
    string_load_from: list[str] = [
        'deathcause_text',
        'container_name',
        'object_prefix',
        'object_name',
        'object_suffix',
        'entity_prefix',
        'entity_name',
        'entity_suffix',
        # region_* will be added in DP4_Core.play with DP4_Core.init_world_files
        # 'region_prefix',
        # 'region_suffix',
    ]

    item_base_value_mod: float = 0.00001

    item_name_unknown_char_value: float = 0.00001
    item_name_char_value: dict[str, float] = {
        'a': 0.00011,
        'b': 0.00022,
        'c': 0.00033,
        'd': 0.00044,
        'e': 0.00055,
        'f': 0.00066,
        'g': 0.00077,
        'h': 0.00088,
        'i': 0.00099,
        'j': 0.00111,
        'k': 0.00122,
        'l': 0.00133,
        'm': 0.00144,
        'n': 0.00155,
        'o': 0.00166,
        'p': 0.00177,
        'q': 0.00188,
        'r': 0.00199,
        's': 0.00211,
        't': 0.00222,
        'u': 0.00233,
        'v': 0.00244,
        'w': 0.00255,
        'x': 0.00266,
        'y': 0.00277,
        'z': 0.00288,
        '0': 0.00011,
        '1': 0.00022,
        '2': 0.00033,
        '3': 0.00044,
        '4': 0.00055,
        '5': 0.00066,
        '6': 0.00077,
        '7': 0.00088,
        '8': 0.00098,
        '9': 0.00099,
    }

    currency_name: str = 'koinz'

    travel_speed: float = 5.3

    inventory_size: int = 20

    end_of_gameloop_duration: tuple[float, float] = (3.0, 5.0)

    sim_wakeup_wakingup_duration: tuple[float, float] = (3.0, 5.0)

    sim_sell_searchvendor_duration: tuple[float, float] = (3.0, 5.0)
    sim_sell_negvendormod_duration: tuple[float, float] = (3.0, 5.0)
    sim_sell_vendormod_range: tuple[float, float] = (0.5, 1.5)
    sim_sell_leavevendor_duration: tuple[float, float] = (3.0, 5.0)

    sim_transfer_currency_treshold: float = 1.0
    sim_transfer_currency_transfer_duration: tuple[float, float] = (3.0, 5.0)
    sim_transfer_currency_transfer_amount_mod: float = 0.75

    sim_walk_walking_duration: tuple[float, float] = (3.0, 5.0)
    sim_walk_enternewregion_duration: tuple[float, float] = (3.0, 5.0)
    sim_walk_startevent_chance: float = 0.13

    sim_death_dying_duration: tuple[float, float] = (3.0, 5.0)

    sim_rebirth_waiting_duration: tuple[float, float] = (3.0, 5.0)
    sim_rebirth_calibrate_duration: tuple[float, float] = (3.0, 5.0)

    sim_gift_approach_duration: tuple[float, float] = (2.0, 5.0)
    sim_gift_opengift_duration: tuple[float, float] = (2.0, 5.0)

    sim_hacker_attack_duration: tuple[float, float] = (3.0, 5.0)
    sim_hacker_hacking_duration: tuple[float, float] = (3.0, 5.0)

    sim_container_checking_duration: tuple[float, float] = (3.0, 5.0)

    sim_entity_attitude: list[str] = ['friendly', 'hostile']
    sim_entity_acting_duration: tuple[float, float] = (3.0, 5.0)
    sim_entity_entityflee_chance_range: tuple[float, float] = (0.0, 0.5)
    sim_entity_playerflee_chance_range: tuple[float, float] = (0.0, 0.5)
    sim_entity_conversation_chance_range: tuple[float, float] = (0.0, 0.5)

    sim_conversation_convo_duration: tuple[float, float] = (3.0, 5.0)

    sim_fight_fighting_duration: tuple[float, float] = (3.0, 5.0)
    sim_fight_searchcorpse_duration: tuple[float, float] = (3.0, 5.0)
    sim_fight_hidecorpse_duration: tuple[float, float] = (3.0, 5.0)
    sim_fight_stolenitemsmin_count: int = 0
    sim_fight_stolenitemsmax_mod: float = 0.3

    sim_find_loot_count: tuple[int, int] = (0, 5)
    sim_find_loot_wagoncheck_duration: tuple[float, float] = (3.0, 5.0)
