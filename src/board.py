from dataclasses import dataclass, field
from .constants import Cell, CELL_DISPLAY, ROWS, COLS, CONNECT_N

@dataclass
class Board:
    """
    Encapsulates the game board and all operations on it.

    The board is stored as a 2-D list of Cell values.
    Row index 0 is the TOP of the board (visually), and row index
    (rows - 1) is the BOTTOM — this matches standard console output
    but means gravity drops pieces toward higher row indices.
    """
    rows: int = ROWS
    cols: int = COLS
    grid: list[list[Cell]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialise an empty grid if none was provided."""
        if not self.grid:
            self.grid = [
                [Cell.EMPTY for _ in range(self.cols)]
                for _ in range(self.rows)
            ]

    # ── Display ───────────────────────────────────────────────────────────

    def display(self) -> None:
        """
        Print the board to the console with column numbers and a neat frame.
        """
        # Column header
        header = "  " + "   ".join(str(c + 1) for c in range(self.cols))
        print(header)

        # Top border
        print("┌" + "┬".join(["───"] * self.cols) + "┐")

        for r in range(self.rows):
            row_str = "│"
            for c in range(self.cols):
                symbol = CELL_DISPLAY[self.grid[r][c]]
                # Colour the pieces for better readability (ANSI codes)
                if self.grid[r][c] == Cell.HUMAN:
                    symbol = f"\033[96m{symbol}\033[0m"   # Cyan for Human
                elif self.grid[r][c] == Cell.AI:
                    symbol = f"\033[91m{symbol}\033[0m"   # Red for AI
                row_str += f" {symbol} │"
            print(row_str)

            # Row separator or bottom border
            if r < self.rows - 1:
                print("├" + "┼".join(["───"] * self.cols) + "┤")
            else:
                print("└" + "┴".join(["───"] * self.cols) + "┘")

    # ── Core Game Operations ──────────────────────────────────────────────

    def get_valid_columns(self) -> list[int]:
        """
        Return a list of column indices where a piece can still be dropped.
        A column is valid if its topmost cell (row 0) is empty.
        """
        return [c for c in range(self.cols) if self.grid[0][c] == Cell.EMPTY]

    def drop_piece(self, col: int, player: Cell) -> int:
        """
        Drop a piece into the given column for the given player.

        Gravity simulation: iterate from the bottom row upward and place
        the piece in the first empty cell encountered.

        Returns:
            The row index where the piece landed.

        Raises:
            ValueError: If the column is full.
        """
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][col] == Cell.EMPTY:
                self.grid[r][col] = player
                return r
        raise ValueError(f"Column {col} is full — cannot drop piece.")

    def remove_piece(self, row: int, col: int) -> None:
        """
        Remove a piece from the specified cell. Used by Minimax to *undo*
        moves after exploring a branch, restoring the board state without
        needing to copy the entire grid.
        """
        self.grid[row][col] = Cell.EMPTY

    def is_full(self) -> bool:
        """Return True if every cell is occupied (draw condition)."""
        return len(self.get_valid_columns()) == 0

    # ── Win Detection ─────────────────────────────────────────────────────

    def check_winner(self, player: Cell) -> bool:
        """
        Check whether the given player has achieved Connect-3.

        Scans horizontal, vertical, and both diagonal directions.
        Returns True as soon as a winning line is found.
        """
        g = self.grid

        # Horizontal check: slide a window of size CONNECT_N across each row
        for r in range(self.rows):
            for c in range(self.cols - CONNECT_N + 1):
                if all(g[r][c + i] == player for i in range(CONNECT_N)):
                    return True

        # Vertical check: slide a window down each column
        for r in range(self.rows - CONNECT_N + 1):
            for c in range(self.cols):
                if all(g[r + i][c] == player for i in range(CONNECT_N)):
                    return True

        # Diagonal check (top-left → bottom-right, i.e. "\" direction)
        for r in range(self.rows - CONNECT_N + 1):
            for c in range(self.cols - CONNECT_N + 1):
                if all(g[r + i][c + i] == player for i in range(CONNECT_N)):
                    return True

        # Diagonal check (bottom-left → top-right, i.e. "/" direction)
        for r in range(CONNECT_N - 1, self.rows):
            for c in range(self.cols - CONNECT_N + 1):
                if all(g[r - i][c + i] == player for i in range(CONNECT_N)):
                    return True

        return False
