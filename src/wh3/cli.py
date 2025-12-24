"""CLI for Warhammer 3 console commands."""

from typing import Annotated

import pyperclip
import typer
from rich.console import Console
from rich.table import Table

from .lords import load_all_characters, load_legendary_lords

app = typer.Typer(help="Warhammer 3 console command helper")
console = Console()

# Load all legendary lords from NDJSON files
LORDS = load_legendary_lords()


def copy_to_clipboard(command: str, lord_name: str) -> None:
    """Copie la commande dans le clipboard et affiche un message."""
    pyperclip.copy(command)
    console.print(f"✓ [green]Command copied to clipboard for {lord_name}:[/green]")
    console.print(f"  [cyan]{command}[/cyan]")


@app.command()
def spawn(lord_name: str) -> None:
    """Generate spawn command for a legendary lord."""
    lord_name_lower = lord_name.lower()

    if lord_name_lower not in LORDS:
        console.print(f"[red]Error:[/red] Lord '{lord_name}' not found.")
        console.print("Use [cyan]wh3 list[/cyan] to see available lords.")
        raise typer.Exit(1)

    faction_obj = LORDS[lord_name_lower]
    command = f"spawn {faction_obj.lord_type} {faction_obj.faction_key}"
    copy_to_clipboard(command, lord_name)


@app.command()
def give(lord_name: str) -> None:
    """Generate give_settlement command for a legendary lord."""
    lord_name_lower = lord_name.lower()

    if lord_name_lower not in LORDS:
        console.print(f"[red]Error:[/red] Lord '{lord_name}' not found.")
        console.print("Use [cyan]wh3 list[/cyan] to see available lords.")
        raise typer.Exit(1)

    faction_obj = LORDS[lord_name_lower]
    command = f"gr {faction_obj.faction_key}"
    copy_to_clipboard(command, lord_name)


@app.command()
def info(lord_name: str) -> None:
    """Display all information about a legendary lord."""
    lord_name_lower = lord_name.lower()

    if lord_name_lower not in LORDS:
        console.print(f"[red]Error:[/red] Lord '{lord_name}' not found.")
        console.print("Use [cyan]wh3 list[/cyan] to see available lords.")
        raise typer.Exit(1)

    faction_obj = LORDS[lord_name_lower]

    table = Table(title=f"Lord Information: {lord_name}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Name", lord_name)
    table.add_row("Faction Key", faction_obj.faction_key)
    table.add_row("Lord Type", faction_obj.lord_type)
    table.add_row("Race", faction_obj.race)
    table.add_row(
        "Spawn Command",
        f"spawn {faction_obj.lord_type} {faction_obj.faction_key}",
    )
    table.add_row("Give Settlement", f"gr {faction_obj.faction_key}")

    console.print(table)


@app.command(name="list")
def list_lords() -> None:
    """List all available legendary lords."""
    from .lords import LegendaryLord

    # Dédupliquer les lords (enlever les alias)
    seen_factions: set[str] = set()
    unique_lords: list[tuple[str, LegendaryLord]] = []

    for name, faction_obj in LORDS.items():
        if faction_obj.faction_key not in seen_factions:
            seen_factions.add(faction_obj.faction_key)
            unique_lords.append((name, faction_obj))

    table = Table(title="Available Legendary Lords")
    table.add_column("Lord Name", style="cyan", no_wrap=True)
    table.add_column("Faction Key", style="yellow")
    table.add_column("Race", style="green")

    for name, faction_obj in sorted(unique_lords, key=lambda x: x[0]):
        table.add_row(name, faction_obj.faction_key, faction_obj.race)

    console.print(table)
    console.print("\n[dim]Use: wh3 <lord_name> spawn|give|info[/dim]")


@app.command()
def cmd(search: str | None = None) -> None:
    """Show common console commands reference.

    Args:
        search: Optional search term to filter commands.

    """
    commands = {
        # Basic commands
        "kill": "Kill/wound selected character and army",
        "confederate": "Confederate selected faction",
        "fff": "Toggle fog of war off",
        "fow on": "Toggle fog of war on",
        "tele": "Teleport (select char, then target, then type)",
        "am": "Restore selected character movement points",
        # Region commands
        "primary": "Set region primary slot to max level",
        "primary <N>": "Set region primary slot to level N",
        "region": "Give 1000 growth + instant building to all regions",
        "region off": "Turn off region bonuses",
        "abandon": "Abandon selected region",
        # Resources
        "give gold": "Give 50000 gold",
        "give gold <N>": "Give N gold (can be negative)",
        # Army/Character
        "heal <N>": "Set army health to N% (0-100)",
        "add xp <N>": "Add N XP to selected character",
        "add axp <N>": "Add N ranks to all units in army",
        # Tech/Diplomacy
        "technology": "Give +2000% research speed",
        "technology <N>": "Give N% research speed",
        "alliance": "Military alliance with selected faction",
        "peace": "Make peace with selected faction",
        "trade": "Trade agreement with selected faction",
        "war": "Start war with selected faction",
    }

    table = Table(title="Console Commands Reference")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for cmd_name, desc in commands.items():
        if (
            search is None
            or search.lower() in cmd_name.lower()
            or search.lower() in desc.lower()
        ):
            table.add_row(cmd_name, desc)

    console.print(table)
    console.print("\n[dim]Use in-game console. Type command and press Enter.[/dim]")


@app.command()
def kill(
    character: Annotated[
        str | None,
        typer.Argument(help="Character art_set_id"),
    ] = None,
) -> None:
    """Kill/wound a character. If character provided, shows info; else copies 'kill' command.

    Args:
        character: Optional character art_set_id for reference.

    """
    if character:
        # Show character info
        characters = load_all_characters()
        if character in characters:
            char = characters[character]
            console.print(f"[cyan]Character:[/cyan] {char.art_set_id}")
            console.print(f"[yellow]Type:[/yellow] {char.agent_type}")
            console.print(f"[green]Subtype:[/green] {char.agent_subtype}")
            console.print(
                "\n[dim]Select character in-game and type:[/dim] [cyan]kill[/cyan]",
            )
        else:
            console.print(f"[red]Error:[/red] Character '{character}' not found.")
            raise typer.Exit(1)
    else:
        # Just copy kill command
        command = "kill"
        copy_to_clipboard(command, "character")


if __name__ == "__main__":
    app()
