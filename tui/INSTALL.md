# HIVEMIND TUI Installation Guide

This guide will help you set up and run the HIVEMIND Terminal User Interface.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- HIVEMIND backend API running (optional for testing)

## Quick Start

### 1. Navigate to TUI Directory

```bash
cd /var/home/mintys/HIVEMIND/tui
```

### 2. Install Dependencies

Install the package in development mode:

```bash
pip install -e .
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

### 3. Configure Environment (Optional)

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` to set your API endpoints:

```bash
HIVEMIND_API_URL=http://localhost:8000
HIVEMIND_WS_URL=ws://localhost:8000
```

### 4. Run the TUI

Using the launcher script:

```bash
./run-tui.sh
```

Or directly with Python:

```bash
hivemind-tui
```

Or with custom endpoints:

```bash
hivemind-tui --api-url http://localhost:8000 --ws-url ws://localhost:8000
```

## Detailed Installation

### Virtual Environment (Recommended)

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

Then install the package:

```bash
pip install -e .
```

### System-Wide Installation

Not recommended for development, but possible:

```bash
pip install .
```

## Verifying Installation

Check that the package is installed:

```bash
python3 -c "import hivemind_tui; print(hivemind_tui.__version__)"
```

Check the command-line tool:

```bash
hivemind-tui --help
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you're in the correct directory and the package is installed:

```bash
pip show hivemind-tui
```

### Missing Dependencies

If you see missing dependency errors, reinstall:

```bash
pip install -e . --force-reinstall
```

### Textual Display Issues

If the TUI doesn't display correctly:

1. Ensure your terminal supports 256 colors
2. Try a different terminal emulator
3. Check terminal size (minimum 80x24 recommended)

### Connection Issues

If you can't connect to the API:

1. Verify the backend is running
2. Check the API URL in your configuration
3. Ensure no firewall is blocking the connection

## Development Mode

For development with hot-reloading CSS:

```bash
./run-tui.sh --watch-css
```

This will automatically reload the CSS when `styles.css` is modified.

## Uninstalling

```bash
pip uninstall hivemind-tui
```

## Next Steps

- Read the [README.md](README.md) for usage instructions
- Explore keyboard shortcuts in the application
- Check out the widget documentation in the source code

## Support

For issues and questions:
- Check the HIVEMIND documentation
- Review the source code in `src/hivemind_tui/`
- Check logs for error messages
