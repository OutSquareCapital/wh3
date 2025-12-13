import polars as pl
import rich

import wh3


def main() -> pl.DataFrame:
    wh3.factions.archaon.spawn()
    wh3.factions.archaon.give_settlement()
    rich.print(wh3.data.factions_df.schema)
    return wh3.data.find_factions("dark_elves")


if __name__ == "__main__":
    main().pipe(print)
