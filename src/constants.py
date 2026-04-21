from enum import IntEnum

class Cell(IntEnum):
    """
    Represents the three possible states of a board cell.
    Using IntEnum allows direct integer comparison while preserving
    readable names in debug output.
    """
    EMPTY = 0
    HUMAN = 1   # Player 1 — 'X'
    AI = 2      # Player 2 — 'O'

# Display characters for each cell state
CELL_DISPLAY: dict[Cell, str] = {
    Cell.EMPTY: "·",   # Middle dot — visually clean empty cell
    Cell.HUMAN: "X",
    Cell.AI: "O",
}

# Board dimensions
ROWS: int = 5
COLS: int = 6

# The number of pieces needed in a row to win
CONNECT_N: int = 3

# Default search depth for the Minimax algorithm.
# Depth 5 provides strong play while remaining very responsive.
DEFAULT_DEPTH: int = 5
