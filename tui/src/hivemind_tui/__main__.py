"""HIVEMIND TUI entry point."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import load_config, TUIConfig
from .styles.themes import get_theme


def setup_logging(config: TUIConfig) -> None:
    """Set up logging.

    Args:
        config: TUI configuration.
    """
    level = getattr(logging, config.log_level.upper(), logging.INFO)

    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    handlers.append(console_handler)

    # File handler if configured
    if config.log_file:
        log_path = Path(config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=handlers,
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="HIVEMIND Terminal User Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hivemind-tui                          # Run with default config
  hivemind-tui --theme hacker           # Use hacker theme
  hivemind-tui --backend http://api:8000  # Connect to specific backend
  hivemind-tui --config ~/.hivemind.json  # Use custom config file

Environment Variables:
  HIVEMIND_THEME           Theme name (dark, light, hacker)
  HIVEMIND_BACKEND_URL     Backend API URL
  HIVEMIND_LOG_LEVEL       Logging level (DEBUG, INFO, WARNING, ERROR)
  HIVEMIND_LOG_FILE        Log file path
        """
    )

    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        help="Path to configuration file",
    )

    parser.add_argument(
        "--theme",
        "-t",
        choices=["dark", "light", "hacker"],
        help="Color theme",
    )

    parser.add_argument(
        "--backend",
        "-b",
        help="Backend API URL",
    )

    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )

    parser.add_argument(
        "--log-file",
        type=Path,
        help="Log file path",
    )

    parser.add_argument(
        "--no-metrics",
        action="store_true",
        help="Disable metrics display",
    )

    parser.add_argument(
        "--no-auto-refresh",
        action="store_true",
        help="Disable auto-refresh",
    )

    parser.add_argument(
        "--refresh-interval",
        type=int,
        help="Auto-refresh interval in seconds",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code.
    """
    # Parse arguments
    args = parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override config with CLI arguments
    if args.theme:
        config.theme = args.theme

    if args.backend:
        config.backend_url = args.backend

    if args.log_level:
        config.log_level = args.log_level

    if args.log_file:
        config.log_file = str(args.log_file)

    if args.no_metrics:
        config.show_metrics = False

    if args.no_auto_refresh:
        config.auto_refresh = False

    if args.refresh_interval:
        config.refresh_interval = args.refresh_interval

    # Set up logging
    setup_logging(config)
    logger = logging.getLogger(__name__)

    try:
        # Validate theme
        theme = get_theme(config.theme)
        logger.info(f"Using theme: {theme.name}")

        # Import and run app
        # Note: Import here to avoid circular dependencies and ensure
        # logging is set up before any app code runs
        from .app import HivemindApp

        logger.info(f"Starting HIVEMIND TUI")
        logger.info(f"Backend URL: {config.backend_url}")
        logger.debug(f"Configuration: {config}")

        # Create and run app
        app = HivemindApp(config=config)
        app.run()

        logger.info("HIVEMIND TUI stopped")
        return 0

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
