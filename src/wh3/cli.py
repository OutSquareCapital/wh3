"""CLI for Warhammer 3 console commands."""

from typing import Annotated

import pyperclip
import typer
from rich.console import Console
from rich.table import Table

from ._consts import COMMANDS
from .lords import LegendaryLord, load_legendary_lords

app = typer.Typer(help="Warhammer 3 console command helper")
console = Console()
LordNameArg = Annotated[str, typer.Argument(help="Name of the legendary lord")]
LORDS = load_legendary_lords()


@app.command()
def spawn(lord_name: LordNameArg) -> None:
    """Generate spawn command for a legendary lord."""
    faction_obj = _get_lord(lord_name)
    command = f"spawn {faction_obj.agent_subtype}"
    _copy_to_clipboard(command, lord_name)


@app.command()
def give(lord_name: LordNameArg) -> None:
    """Generate give_settlement command for a legendary lord."""
    faction_obj = _get_lord(lord_name)
    command = f"gr {faction_obj.faction_key}"
    _copy_to_clipboard(command, lord_name)


@app.command()
def info(lord_name: LordNameArg) -> None:
    """Display all information about a legendary lord."""
    faction_obj = _get_lord(lord_name)

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
def list_lords(
    race: Annotated[
        str | None,
        typer.Argument(help="Optional race filter (e.g., dwf, grn, emp)"),
    ] = None,
) -> None:
    """List all available legendary lords."""

    def _add_to_table(table: Table) -> None:
        def _add_to_list(faction_obj: LegendaryLord) -> bool:
            return race is None or faction_obj.race.lower() == race.lower()

        return (
            LORDS.iter()
            .filter(lambda x: _add_to_list(x.value))
            .sort(
                key=lambda x: x.key,
            )
            .iter()
            .for_each(
                lambda x: table.add_row(x.key, x.value.faction_key, x.value.race),
            )
        )

    table = Table(title="Available Legendary Lords")
    table.add_column("Lord Name", style="cyan", no_wrap=True)
    table.add_column("Faction Key", style="yellow")
    table.add_column("Race", style="green")
    _add_to_table(table)

    console.print(table)
    if race:
        console.print(f"\n[dim]Showing lords for race: {race}[/dim]")
    console.print("\n[dim]Use: wh3 <lord_name> spawn|give|info[/dim]")


@app.command()
def cmd(
    search: Annotated[
        str | None,
        typer.Argument(help="Optional search term to filter commands"),
    ] = None,
) -> None:
    """Show common console commands reference."""
    table = Table(title="Console Commands Reference")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    COMMANDS.iter().filter(
        lambda x: search is None
        or search.lower() in x.key.lower()
        or search.lower() in x.value.lower(),
    ).for_each(lambda x: table.add_row(x.key, x.value))

    console.print(table)
    console.print("\n[dim]Use in-game console. Type command and press Enter.[/dim]")


def _get_lord(lord_name: str) -> LegendaryLord:
    def _not_found() -> typer.Exit:
        console.print(f"[red]Error:[/red] Lord '{lord_name}' not found.")
        console.print("Use [cyan]wh3 list[/cyan] to see available lords.")
        return typer.Exit(1)

    return LORDS.get_item(lord_name.lower()).ok_or_else(_not_found).unwrap()


def _copy_to_clipboard(command: str, lord_name: str) -> None:
    pyperclip.copy(command)
    console.print(f"✓ [green]Command copied to clipboard for {lord_name}:[/green]")
    console.print(f"  [cyan]{command}[/cyan]")


if __name__ == "__main__":
    app()
