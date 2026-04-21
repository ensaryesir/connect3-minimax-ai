import sys
from src.constants import DEFAULT_DEPTH
from src.game import Game

# ── Ensure UTF-8 output on Windows ───────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

def main() -> None:
    """Parse optional CLI arguments and start the game."""
    depth = DEFAULT_DEPTH
    if len(sys.argv) > 1:
        try:
            depth = int(sys.argv[1])
            if depth < 1:
                raise ValueError
        except ValueError:
            print(f"Usage: python {sys.argv[0]} [depth]")
            print(f"  depth : positive integer (default={DEFAULT_DEPTH})")
            sys.exit(1)

    game = Game(ai_depth=depth)
    game.play()

if __name__ == "__main__":
    main()
