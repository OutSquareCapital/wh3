from dataclasses import dataclass

from ._core import FactionCommand


@dataclass
class Chaos(FactionCommand):
    lord = "wh_main_chs_lord"
    _leader = "wh_main_chs_archaon"
    race = "chs"


@dataclass
class Greenskin(FactionCommand):
    lord = "wh_main_grn_orc_warboss"
    race = "grn"


@dataclass
class Norsca(FactionCommand):
    lord = "wh_main_nor_marauder_chieftain"
    race = "nor"


@dataclass
class Kislev(FactionCommand):
    lord = "wh3_main_ksl_boyar"
    race = "ks"


@dataclass
class Skaven(FactionCommand):
    lord = "wh2_main_skv_warlord"
    race = "skv"


@dataclass
class Empire(FactionCommand):
    lord = "wh_main_emp_lord"
    race = "emp"


@dataclass
class Lizardmen(FactionCommand):
    lord = "wh2_main_lzd_saurus_old_blood"
    race = "lzd"


@dataclass
class Beastmen(FactionCommand):
    lord = "wh_dlc03_bst_beastlord"
    race = "bst"


@dataclass
class Dwarf(FactionCommand):
    lord = "wh_main_dwf_lord"
    race = "dwf"


@dataclass
class DarkElf(FactionCommand):
    lord = "wh2_main_def_dreadlord"
    race = "def"
