"""Load and manage legendary lords data from NDJSON files."""

from typing import NamedTuple, Self

import polars as pl
import pyochain as pc

from ._consts import LORD_TYPE, Race, RaceType
from ._schemas import Data


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

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Self:
        """Create **Self** from a Polars DataFrame row."""
        return cls(
            name=row["display_name"],
            agent_subtype=row["agent_subtype"],
            faction_key=row["faction_key"],
            lord_type=row["lord_type"],
            race=row["race"],
        )


def load_legendary_lords() -> pc.Dict[str, LegendaryLord]:
    """Load all legendary lords from NDJSON files."""
    return (
        Data.agents.scan(
            ignore_errors=True,
        )
        .filter(
            pl.col("recruitment_category").eq("legendary_lords"),
            pl.col("auto_generate").not_(),
        )
        .select(pl.col("key").alias("agent_subtype"))
        # Join with frontend_faction_leaders to get the faction mapping
        .join(
            Data.frontend_faction_leaders.scan(ignore_errors=True).select(
                pl.col("agent_subtype_record").alias("agent_subtype"),
                pl.col("faction").alias("faction_key"),
            ),
            on="agent_subtype",
            how="left",
        )
        # Extract race from faction_key
        .with_columns(
            pl.col("faction_key").pipe(_race_from_faction_key),
            pl.col("agent_subtype").pipe(_clean_display_name),
        )
        .join(
            pl.LazyFrame(
                {
                    "race": pc.Iter(Race).into(pl.Series, dtype=RaceType),
                    "lord_type": LORD_TYPE,
                },
            ),
            on="race",
            how="left",
        )
        .collect()
        .pipe(lambda df: pc.Iter(df.iter_rows(named=True)))
        .map(
            lambda row: (
                row["display_name"],
                LegendaryLord.from_row(row),
            ),
        )
        .into(pc.Dict)
    )


def _race_from_faction_key(expr: pl.Expr) -> pl.Expr:
    return (
        expr.str.extract(r"(?:main|dlc\d+|pro\d+|twa\d+)_([a-z]+)", 1)
        .cast(RaceType)
        .alias("race")
    )


def _clean_display_name(expr: pl.Expr) -> pl.Expr:
    return (
        expr.str.replace_all(r"^wh\d?_", "")
        .str.replace_all(r"dlc\d+_", "")
        .str.replace_all(r"pro\d+_", "")
        .str.replace_all(r"twa\d+_", "")
        .str.replace_all("main_", "")
        .str.replace_all(r"_\d+", "")
        .alias("display_name")
    )
