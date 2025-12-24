"""CLI for Warhammer 3 console commands."""

from typing import Annotated

import pyochain as pc
import pyperclip
import typer
from rich.console import Console
from rich.table import Table

from ._core import COMMANDS
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
    command = f"spawn {faction_obj.agent_subtype}"
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
    table.add_row("Agent Subtype", faction_obj.agent_subtype)
    table.add_row("Faction Key", faction_obj.faction_key)
    table.add_row("Lord Type", faction_obj.lord_type)
    table.add_row("Race", faction_obj.race)
    table.add_row(
        "Spawn Command",
        f"spawn {faction_obj.agent_subtype}",
    )
    table.add_row("Give Settlement", f"gr {faction_obj.faction_key}")

    console.print(table)


@app.command(name="list")
def list_lords(race: str | None = None) -> None:
    """List all available legendary lords.

    Args:
        race: Optional race filter (e.g., dwf, grn, emp).

    """
    from .lords import LegendaryLord

    def _add_to_list(faction_obj: LegendaryLord) -> bool:
        return race is None or faction_obj.race.lower() == race.lower()

    table = Table(title="Available Legendary Lords")
    table.add_column("Lord Name", style="cyan", no_wrap=True)
    table.add_column("Faction Key", style="yellow")
    table.add_column("Race", style="green")

    pc.Iter(LORDS.items()).filter(lambda x: _add_to_list(x[1])).sort(
        key=lambda x: x[0],
    ).iter().for_each(
        lambda x: table.add_row(x[0], x[1].faction_key, x[1].race),
    )

    console.print(table)
    if race:
        console.print(f"\n[dim]Showing lords for race: {race}[/dim]")
    console.print("\n[dim]Use: wh3 <lord_name> spawn|give|info[/dim]")


@app.command()
def cmd(search: str | None = None) -> None:
    """Show common console commands reference.

    Args:
        search: Optional search term to filter commands.

    """
    table = Table(title="Console Commands Reference")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    COMMANDS.iter().filter(
        lambda x: search is None
        or search.lower() in x[0].lower()
        or search.lower() in x[1].lower(),
    ).for_each(lambda x: table.add_row(*x))

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
