from enum import StrEnum, auto

import polars as pl
import pyochain as pc

COMMANDS = pc.Dict(
    {
        # Basic commands
        "kill": "Kill/wound selected character and army",
        "confederate": "Confederate selected faction",
        "fff": "Toggle fog of war off",
        "fow on": "Toggle fog of war on",
        "tele": "Teleport (select char, then target, then type)",
        "am": "Restore selected character movement points",
        # Region commands
        "primary": "Set region primary slot to max level",
        "primary <N>": "Set region primary slot to level N",
        "region": "Give 1000 growth + instant building to all regions",
        "region off": "Turn off region bonuses",
        "abandon": "Abandon selected region",
        # Resources
        "give gold": "Give 50000 gold",
        "give gold <N>": "Give N gold (can be negative)",
        # Army/Character
        "heal <N>": "Set army health to N% (0-100)",
        "add xp <N>": "Add N XP to selected character",
        "add axp <N>": "Add N ranks to all units in army",
        # Tech/Diplomacy
        "technology": "Give +2000% research speed",
        "technology <N>": "Give N% research speed",
        "alliance": "Military alliance with selected faction",
        "peace": "Make peace with selected faction",
        "trade": "Trade agreement with selected faction",
        "war": "Start war with selected faction",
    },
)
LORD_TYPE = (  # TODO: why is this hardcoded? need to be loaded from data.
    "wh_main_chs_lord",
    "wh_main_grn_orc_warboss",
    "wh_main_nor_marauder_chieftain",
    "wh3_main_ksl_boyar",
    "wh2_main_skv_warlord",
    "wh_main_emp_lord",
    "wh2_main_lzd_saurus_old_blood",
    "wh_dlc03_bst_bray_shaman_beasts",
    "wh_main_dwf_lord",
    "wh2_main_def_dreadlord",
    "wh2_main_hef_prince",
    "wh_main_vmp_vampire",
    "wh2_dlc09_tmb_tomb_king",
    "wh_main_brt_lord",
    "wh_dlc05_wef_glade_lord",
    "wh3_main_vmp_vampire_count",
    "wh3_main_ogr_tyrant",
    "wh3_main_kho_exalted_bloodthirster",
    "wh3_main_nur_exalted_great_unclean_one",
    "wh3_main_sla_exalted_keeper_of_secrets",
    "wh3_main_tze_exalted_lord_of_change",
    "wh3_main_dae_daemon_prince",
    "wh3_main_cth_dragon-blooded_shugengan_lord",
    "wh2_dlc11_cst_admiral_death",
    "wh3_dlc23_chd_sorcerer_prophet_death",
)


class Race(StrEnum):
    """Race abreviations identifiers."""

    CHS = auto()
    GRN = auto()
    NOR = auto()
    KSL = auto()
    SKV = auto()
    EMP = auto()
    LZD = auto()
    BST = auto()
    DWF = auto()
    DEF = auto()
    HEF = auto()
    VMP = auto()
    TMB = auto()
    BRT = auto()
    WEF = auto()
    VCO = auto()
    OGR = auto()
    KHO = auto()
    NUR = auto()
    SLA = auto()
    TZE = auto()
    DAE = auto()
    CTH = auto()
    CST = auto()
    CHD = auto()


RaceType = pl.Enum(Race)
"""DataType of the races abreviations."""
