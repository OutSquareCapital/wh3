"""Load and manage legendary lords data from NDJSON files."""

from dataclasses import dataclass
from typing import NamedTuple

import polars as pl
import pyochain as pc

from ._core import AGENTS, CHARACTERS, FRONTEND_FACTION_LEADERS, LORD_TYPE, RACE
from ._schemas import AGENTS as AGENTS_SCHEMA
from ._schemas import CHARACTERS as CHARACTERS_SCHEMA


class LegendaryLord(NamedTuple):
    """Legendary lord with all associated data."""

    name: str
    """Display name (from agent_subtype)."""
    agent_subtype: str
    """Agent subtype for spawn command."""
    faction_key: str
    """Faction key for gr (give settlement) command."""
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
        # Join with frontend_faction_leaders to get the TRUE faction mapping
        .join(
            pl.scan_csv(
                FRONTEND_FACTION_LEADERS,
                separator="\t",
                has_header=True,
                skip_rows_after_header=1,  # Skip the metadata row after header
            ).select(
                pl.col("agent_subtype_record").alias("agent_subtype"),
                pl.col("faction").alias("faction_key"),
            ),
            on="agent_subtype",
            how="left",
        )
        # Fallback: if no faction found, use agent_subtype as faction_key
        .with_columns(
            pl.when(pl.col("faction_key").is_null())
            .then(pl.col("agent_subtype"))
            .otherwise(pl.col("faction_key"))
            .alias("faction_key"),
        )
        # Extract race from faction_key
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
        .join(
            pl.LazyFrame(
                {
                    "race": RACE,
                    "lord_type": LORD_TYPE,
                },
            ),
            on="race",
            how="left",
        )
        .with_columns(
            pl.col("lord_type").fill_null("wh_main_emp_lord"),
        )
        .collect()
        .pipe(lambda df: pc.Iter(df.iter_rows(named=True)))
        .map(
            lambda row: (
                row["display_name"],
                LegendaryLord(
                    name=row["display_name"],
                    agent_subtype=row["agent_subtype"],
                    faction_key=row["faction_key"],
                    lord_type=row["lord_type"],
                    race=row["race"],
                ),
            ),
        )
        .into(dict)
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
        .pipe(lambda df: pc.Iter(df.iter_rows(named=True)))
        .map(
            lambda row: (
                row["art_set_id"],
                Character(
                    art_set_id=row["art_set_id"],
                    agent_type=row["agent_type"],
                    agent_subtype=row["agent_subtype"],
                ),
            ),
        )
        .into(dict)
    )


def get_character_names() -> list[str]:
    """Get list of all character art_set_ids for autocompletion.

    Returns:
        Sorted list of character art_set_ids.

    """
    return sorted(load_all_characters().keys())
