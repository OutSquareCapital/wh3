from pathlib import Path

import framelib as fl


class Paths:
    FRONTEND_FACTION_LEADERS = Path("data").joinpath(
        "db/frontend_faction_leaders_tables/data__.tsv",
    )


class Agents(fl.Schema):
    key = fl.String()
    auto_generate = fl.Boolean()
    is_caster = fl.Boolean()
    small_icon = fl.String()
    associated_unit_override = fl.String()
    audio_voiceover_actor_group = fl.String()
    show_in_ui = fl.Boolean()
    cap = fl.Int64()
    has_female_name = fl.Boolean()
    can_gain_xp = fl.Boolean()
    loyalty_is_applicable = fl.Boolean()
    contributes_to_agent_cap = fl.Boolean()
    recruitment_category = fl.String()
    magic_lore = fl.String()
    names_group = fl.String()  # TODO: check if Null
    can_be_loaned = fl.Boolean()
    recruitable = fl.Boolean()
    saving_settings = fl.String()
    audio_vo_culture_override = fl.String()  # TODO: check if Null
    spam_click_vo_enabled = fl.Boolean()
    can_equip_ancillaries = fl.Boolean()
    cost = fl.Int64()
    recruitment_button_active_icon_path = fl.String()  # TODO: check if Null
    recruitment_button_background_icon_path = fl.String()  # TODO: check if Null


class Characters(fl.Schema):
    art_set_id = fl.String()
    agent_type = fl.String()
    culture = fl.String()  # TODO: check if Null
    subculture = fl.String()  # TODO: check if Null
    faction = fl.String()  # TODO: check if Null
    is_custom = fl.Boolean()
    is_male = fl.Boolean()
    agent_subtype = fl.String()
    campaign_map_scale = fl.Float64()


class Factions(fl.Schema):
    banner_colour_tertiary = fl.String()
    override_target_unit_vo_culture = fl.Boolean()
    movie_death_event = fl.Int64()
    alt_secondary_colour_hex = fl.Int64()
    flags_path = fl.String()
    faction_swapping_id = fl.String()
    cdir_military_generator_config = fl.String()
    neutral_reinforcement_factions = fl.String()
    uniform_colour_primary = fl.String()
    ui_main_theme_skin = fl.String()
    win_movie = fl.String()  # TODO: check if Null
    is_quest_faction = fl.Boolean()
    index = fl.Int64()
    is_rebel = fl.Boolean()
    waaagh_faction = fl.String()  # TODO: check if Null
    subculture = fl.String()
    key = fl.String()
    category = fl.String()
    unit_regiment_name_group = fl.String()
    waaagh_general_unit = fl.String()
    default_audio_actor_vo_group = fl.String()
    text_replacement_key = fl.String()
    music_feedback_group = fl.String()
    primary_colour_hex = fl.String()
    alt_primary_colour_hex = fl.Float64()
    banner_colour_secondary = fl.String()
    ship_name_group = fl.String()
    mp_force_gen_template = fl.String()
    name_group = fl.String()
    feature_forest = fl.String()
    can_accept_gifts_when_dead = fl.Boolean()
    uniform_colour_secondary = fl.String()
    banner_colour_primary = fl.String()
    secondary_colour_hex = fl.String()
    alt_uniform_colour_hex = fl.Int64()
    uniform_colour_hex = fl.Int64()
    rebel_colour_hex = fl.Int64()
    pre_battle_speech_parameter = fl.String()
    primary_colour = fl.String()
    skin = fl.String()
    card_colour_hex = fl.Int64()
    military_group = fl.String()
    ui_skin = fl.String()
    audio_voiceover_culture = fl.String()
    uniform_colour_tertiary = fl.String()


class Data(fl.Folder):
    agents = fl.NDJson(model=Agents)
    characters = fl.NDJson(model=Characters)
    factions = fl.NDJson(model=Factions)
