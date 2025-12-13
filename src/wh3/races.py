from ._core import FactionCommand


class Chaos(FactionCommand):
    _lord = "wh_main_chs_lord"
    _leader = "wh_main_chs_archaon"
    race = "chs"


class Greenskin(FactionCommand):
    _lord = "wh_main_grn_orc_warboss"
    race = "grn"


class Norsca(FactionCommand):
    _lord = "wh_main_nor_marauder_chieftain"
    race = "nor"


class Kislev(FactionCommand):
    _lord = "wh3_main_ksl_boyar"
    race = "ks"


class Skaven(FactionCommand):
    _lord = "wh2_main_skv_warlord"
    race = "skv"


class Empire(FactionCommand):
    _lord = "wh_main_emp_lord"
    race = "emp"


class Lizardmen(FactionCommand):
    _lord = "wh2_main_lzd_saurus_old_blood"
    race = "lzd"


class Beastmen(FactionCommand):
    _lord = "wh_dlc03_bst_beastlord"
    race = "bst"


class Dwarf(FactionCommand):
    _lord = "wh_main_dwf_lord"
    race = "dwf"
