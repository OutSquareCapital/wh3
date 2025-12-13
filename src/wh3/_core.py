from enum import StrEnum, auto
from pathlib import Path

DATA = Path("data")
AGENTS = DATA.joinpath("agents.ndjson")
CHARACTERS = DATA.joinpath("characters.ndjson")
FACTIONS = DATA.joinpath("factions.ndjson")


class DBKeys(StrEnum):
    FACTION_KEY = "key"
    AGENT_SUBTYPE = auto()
    AGENT_TYPE = auto()


class FactionCommand:
    """Faction command class to hold faction commands and their types.

    Must be implemented with class attributes lord and race.
    """

    _lord: str
    race: str

    def __init__(self, faction: str) -> None:
        self.faction: str = faction

    def spawn(self) -> None:
        """Spawns an army next to selected character or settlement.

        Use agent_subtype in the Character art sets table,
        where the agent_type is "lord"
        """
        print(f"spawn {self._lord} {self.faction}")

    def give_settlement(self) -> None:
        """Gives <faction_key> ownership of the selected region.

        If a faction has no regions or armies on the map you can't give them a region, spawn them an army first.
        """
        print(f"gr {self.faction}")


class GenericCommand:
    def kill_lord(self) -> None:
        print("kill")

    def set_region_lvl_to_max(self) -> None:
        """Set primary slot level of selected region to max."""
        print("primary")

    def set_region_lvl_to(self, lvl: int) -> None:
        """Set primary slot level of selected region to <number>."""
        print(f"primary {lvl}")

    def confederate(self) -> None:
        """Confederate the owner of the currently selected settlement or character.

        If a faction has no regions or armies on the map you can't confederate them, spawn them an army first.
        """
        print("confederate")
