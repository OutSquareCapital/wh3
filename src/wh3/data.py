import polars as pl

from ._core import AGENTS, CHARACTERS, FACTIONS, DBKeys

factions_df = pl.read_ndjson(FACTIONS, ignore_errors=True)
agents_df = pl.read_ndjson(AGENTS, ignore_errors=True)
characters_df = pl.read_ndjson(
    CHARACTERS,
    ignore_errors=True,
)


def get_all_factions() -> pl.DataFrame:
    return factions_df.select(DBKeys.FACTION_KEY).unique().sort(DBKeys.FACTION_KEY)


def find_factions(race_name: str) -> pl.DataFrame:
    return factions_df.pipe(
        _search,
        col=DBKeys.FACTION_KEY,
        pattern=race_name,
        result_col=DBKeys.FACTION_KEY,
    )


def find_lords(faction_name: str) -> pl.DataFrame:
    return agents_df.pipe(
        _search,
        col=DBKeys.AGENT_TYPE,
        pattern="general",
        result_col=DBKeys.AGENT_SUBTYPE,
    ).pipe(
        _search,
        col=DBKeys.AGENT_SUBTYPE,
        pattern=faction_name,
        result_col=DBKeys.AGENT_SUBTYPE,
    )


def _search(df: pl.DataFrame, col: str, pattern: str, result_col: str) -> pl.DataFrame:
    return df.filter(pl.col(col).str.contains(pattern)).select(result_col)
