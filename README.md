# WH3 Console Command Helper 🎮

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simple CLI tool for **Total War: Warhammer III** that simplifies the use of console commands with the [Console Command Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2791241084).

This tool provides an intuitive interface to search, generate, and copy console commands directly to your clipboard!

## ✨ Features

- 🔍 **Quick Lord Search**: Find legendary lords by name or race
- 📋 **Auto-Copy Commands**: Generated commands are automatically copied to clipboard
- 🎯 **Spawn Commands**: Generate spawn commands for any legendary lord
- 🏰 **Settlement Commands**: Generate give settlement commands based on faction keys
- 📊 **Detailed Info**: View all data for any legendary lord (agent subtype, faction key, race, etc.)
- 📚 **Command Reference**: Browse all available console commands with descriptions
- 🌈 **Beautiful Output**: Rich terminal UI with colors and formatted tables

## 📦 Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Install uv first if you haven't already:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then clone and install the project:

```bash
git clone <your-repo-url>
cd wh3
uv sync
```

## 🚀 Usage

### List All Legendary Lords

```bash
uv run wh3 list
```

Filter by race:

```bash
uv run wh3 list emp    # Empire lords only
uv run wh3 list skv    # Skaven lords only
```

### Spawn a Legendary Lord

Generate a spawn command and copy it to clipboard:

```bash
uv run wh3 spawn karl_franz
# Output: ✓ Command copied to clipboard: spawn wh_main_emp_karl_franz
```

Then in-game:

1. Open the console (`` ` `` key by default)
2. Paste the command (`Ctrl+V`)
3. Press Enter

### Give Settlement to a Faction

Generate a command to give settlements to a legendary lord's faction:

```bash
uv run wh3 give grimgor_ironhide
# Output: ✓ Command copied to clipboard: gr wh_main_grn_greenskins
```

### View Lord Information

Display detailed information about a legendary lord:

```bash
uv run wh3 info miao_ying
```

Output:

```text
┌─────────────────────────────────────────────────┐
│          Lord Information: miao_ying            │
├─────────────────┬───────────────────────────────┤
│ Name            │ miao_ying                     │
│ Agent Subtype   │ wh3_main_cth_miao_ying        │
│ Faction Key     │ wh3_main_cth_the_northern_... │
│ Lord Type       │ wh3_main_cth_dragon-blooded...│
│ Race            │ cth                           │
│ Spawn Command   │ spawn wh3_main_cth_miao_ying  │
│ Give Settlement │ gr wh3_main_cth_the_norther...│
└─────────────────┴───────────────────────────────┘
```

### Browse Console Commands

View all available console commands:

```bash
uv run wh3 cmd
```

Search for specific commands:

```bash
uv run wh3 cmd gold    # Show only gold-related commands
uv run wh3 cmd heal    # Show heal commands
```

## 📖 Command Reference

### Available Commands

| Command | Description |
| ------- | ----------- |
| `wh3 list [race]` | List all legendary lords (optionally filtered by race) |
| `wh3 spawn <lord_name>` | Generate spawn command for a lord |
| `wh3 give <lord_name>` | Generate give settlement command for a lord's faction |
| `wh3 info <lord_name>` | Display detailed information about a lord |
| `wh3 cmd [search]` | Show console commands reference (optionally filtered) |

Data is processed using [Polars](https://www.pola.rs/) for fast and efficient queries.

## 🛠️ Development

### Project Structure

```text
wh3/
├── src/wh3/
│   ├── cli.py          # Main CLI interface
│   ├── lords.py        # Legendary lords data loading
│   ├── _consts.py      # Constants and command mappings
│   └── _schemas.py     # Data schemas
├── data/               # Game data files
├── pyproject.toml      # Project configuration
└── README.md
```

### Dependencies

- **[Polars](https://www.pola.rs/)**: Fast DataFrame library for data processing
- **[Typer](https://typer.tiangolo.com/)**: CLI framework
- **[Rich](https://rich.readthedocs.io/)**: Beautiful terminal output
- **[Pyperclip](https://pypi.org/project/pyperclip/)**: Cross-platform clipboard access
- **[Pyochain](https://github.com/your-repo/pyochain)**: Functional programming utilities

### Running Tests

```bash
# TODO: Add tests
uv run pytest
```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Creative Assembly for Total War: Warhammer III
- [Console Command Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2791241084) creators
- The Total War modding community

## 🔗 Links

- [Console Command Mod on Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2791241084)
- [Total War: Warhammer III](https://www.totalwar.com/games/warhammer-iii/)

---

Made with ❤️ for the Total War: Warhammer III community
