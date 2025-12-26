"""HIVEMIND TUI entry point - v3.0."""

import os
import sys


def main() -> int:
    """Main entry point."""
    # Store launch directory for context
    os.environ["HIVEMIND_LAUNCH_DIR"] = os.getcwd()

    try:
        from .app import HivemindApp, main as app_main

        # Use the app's main function
        app_main()
        return 0

    except KeyboardInterrupt:
        return 130

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
