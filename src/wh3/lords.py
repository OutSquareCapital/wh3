"""Load and manage legendary lords data from NDJSON files."""

from dataclasses import dataclass
from typing import NamedTuple

import polars as pl

from ._core import AGENTS, CHARACTERS, FACTIONS
from ._schemas import AGENTS as AGENTS_SCHEMA
from ._schemas import CHARACTERS as CHARACTERS_SCHEMA
from ._schemas import FACTIONS as FACTIONS_SCHEMA


def _race_mapping() -> pl.LazyFrame:
    return pl.LazyFrame(
        {
            "race": [
                "chs",
                "grn",
                "nor",
                "ksl",
                "skv",
                "emp",
                "lzd",
                "bst",
                "dwf",
                "def",
                "hef",
                "vmp",
                "tmb",
                "brt",
                "wef",
                "vco",
                "ogr",
                "kho",
                "nur",
                "sla",
                "tze",
                "dae",
                "cth",
            ],
            "lord_type": [
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
            ],
        },
    )


class LegendaryLord(NamedTuple):
    """Legendary lord with all associated data."""

    name: str
    """Display name (from agent_subtype)."""
    faction_key: str
    """Faction key associated with the lord (for commands)"""
    lord_type: str
    """Generic lord type for spawning (e.g., wh_main_emp_lord)"""
    race: str
    """Race abbreviation (e.g., emp, chs, skv)"""


def load_legendary_lords() -> dict[str, LegendaryLord]:
    """Load all legendary lords from NDJSON files.

    Returns:
        Dictionary mapping lord name to LegendaryLord object

    """
    return (
        pl.scan_ndjson(AGENTS, schema=AGENTS_SCHEMA, ignore_errors=True)
        .filter(
            pl.col("recruitment_category").eq("legendary_lords"),
            pl.col("auto_generate").not_(),
        )
        .select(pl.col("key").alias("agent_subtype"))
        # Cross join with factions to find best match
        .join(
            pl.scan_ndjson(FACTIONS, schema=FACTIONS_SCHEMA, ignore_errors=True).select(
                "key",
                "default_audio_actor_vo_group",
            ),
            how="cross",
        )
        # Match: faction key contains agent_subtype OR audio group contains it
        .with_columns(
            pl.col("key")
            .str.contains(pl.col("agent_subtype"))
            .or_(
                pl.col("default_audio_actor_vo_group")
                .str.contains(pl.col("agent_subtype"))
                .fill_null(value=False),
            )
            .alias("is_match"),
        )
        # Keep only matches, or fallback to agent_subtype as faction_key
        .sort("is_match", descending=True)
        .group_by("agent_subtype")
        .agg(
            pl.when(pl.col("is_match").any())
            .then(pl.col("key").filter(pl.col("is_match")).first())
            .otherwise(pl.col("agent_subtype").first())
            .alias("faction_key"),
        )
        # Extract race from faction_key using regex
        .with_columns(
            pl.col("faction_key")
            .str.extract(r"(?:main|dlc\d+|pro\d+|twa\d+)_([a-z]+)", 1)
            .fill_null("unknown")
            .alias("race"),
        )
        # Clean display name
        .with_columns(
            pl.col("agent_subtype")
            .str.replace_all(r"^wh\d?_", "")
            .str.replace_all(r"dlc\d+_", "")
            .str.replace_all(r"pro\d+_", "")
            .str.replace_all(r"twa\d+_", "")
            .str.replace_all("main_", "")
            .str.replace_all(r"_\d+", "")
            .alias("display_name"),
        )
        .join(_race_mapping(), on="race", how="left")
        .with_columns(
            pl.col("lord_type").fill_null("wh_main_emp_lord"),
        )
        .collect()
        .pipe(
            lambda df: {
                row["display_name"]: LegendaryLord(
                    name=row["display_name"],
                    faction_key=row["faction_key"],
                    lord_type=row["lord_type"],
                    race=row["race"],
                )
                for row in df.iter_rows(named=True)
            },
        )
    )


@dataclass
class Character:
    """Character from the game."""

    art_set_id: str
    """Unique art set identifier."""
    agent_type: str
    """Type: general, wizard, spy, etc."""
    agent_subtype: str
    """Specific subtype identifier."""


def load_all_characters() -> dict[str, Character]:
    """Load all characters from NDJSON file.

    Returns:
        Dictionary mapping art_set_id to Character object.

    """
    return (
        pl.read_ndjson(CHARACTERS, schema=CHARACTERS_SCHEMA, ignore_errors=True)
        .filter(
            pl.col("agent_type").is_not_null(),
            pl.col("agent_subtype").is_not_null(),
            pl.col("is_custom").not_(),
        )
        .select("art_set_id", "agent_type", "agent_subtype")
        .sort("")
        .pipe(
            lambda df: {
                row["art_set_id"]: Character(
                    art_set_id=row["art_set_id"],
                    agent_type=row["agent_type"],
                    agent_subtype=row["agent_subtype"],
                )
                for row in df.iter_rows(named=True)
            },
        )
    )


def get_character_names() -> list[str]:
    """Get list of all character art_set_ids for autocompletion.

    Returns:
        Sorted list of character art_set_ids.

    """
    return sorted(load_all_characters().keys())
