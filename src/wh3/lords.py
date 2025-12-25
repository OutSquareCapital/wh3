"""Load and manage legendary lords data from NDJSON files."""

import polars as pl
import pyochain as pc

from ._consts import LORD_TYPE, Race, RaceType
from ._models import Character, LegendaryLord
from ._schemas import Agents, Characters, Data, Paths


def load_all_characters() -> pc.Dict[str, Character]:
    """Load all characters from NDJSON file."""
    return (
        Data.characters.scan(
            schema=Characters.pl_schema(),
            ignore_errors=True,
        )
        .filter(
            pl.col("agent_type").is_not_null(),
            pl.col("agent_subtype").is_not_null(),
            pl.col("is_custom").not_(),
        )
        .select("art_set_id", "agent_type", "agent_subtype")
        .sort("")
        .collect()
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
        .into(pc.Dict.from_)
    )


def load_legendary_lords() -> pc.Dict[str, LegendaryLord]:
    """Load all legendary lords from NDJSON files."""
    return (
        Data.agents.scan(
            schema=Agents.pl_schema(),
            ignore_errors=True,
        )
        .filter(
            pl.col("recruitment_category").eq("legendary_lords"),
            pl.col("auto_generate").not_(),
        )
        .select(pl.col("key").alias("agent_subtype"))
        # Join with frontend_faction_leaders to get the TRUE faction mapping
        .join(
            pl.scan_csv(
                Paths.FRONTEND_FACTION_LEADERS,
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
                LegendaryLord(
                    name=row["display_name"],
                    agent_subtype=row["agent_subtype"],
                    faction_key=row["faction_key"],
                    lord_type=row["lord_type"],
                    race=row["race"],
                ),
            ),
        )
        .into(pc.Dict.from_)
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
