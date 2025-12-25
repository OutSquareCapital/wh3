from typing import NamedTuple


class Character(NamedTuple):
    """Character from the game."""

    art_set_id: str
    """Unique art set identifier."""
    agent_type: str
    """general, wizard, spy, etc."""
    agent_subtype: str
    """Specific subtype identifier."""


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
