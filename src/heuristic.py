from .constants import Cell, CONNECT_N
from .board import Board

def _score_window(window: list[Cell]) -> int:
    """
    Evaluate a single window of CONNECT_N cells and return a heuristic score.
    """
    ai_count = window.count(Cell.AI)
    human_count = window.count(Cell.HUMAN)
    empty_count = window.count(Cell.EMPTY)

    # ── Scoring rules ─────────────────────────────────────────────────────
    if ai_count == 3:
        return 100       # AI has already won in this window
    if ai_count == 2 and empty_count == 1:
        return 10        # AI is one move away from completing this line
    if ai_count == 1 and empty_count == 2:
        return 1         # AI has a piece here — early-stage potential

    if human_count == 3:
        return -100      # Human has won in this window
    if human_count == 2 and empty_count == 1:
        return -10       # Human threatens to complete this line

    return 0             # Mixed or empty — no strategic value


def evaluate_board(board: Board) -> int:
    """
    Compute the full heuristic evaluation of the board for the AI player.
    """
    score: int = 0
    g = board.grid

    # ── 1. Centre-Column Bonus ────────────────────────────────────────────
    centre_cols: list[int] = [board.cols // 2]
    if board.cols % 2 == 0:
        centre_cols.append(board.cols // 2 - 1)

    for c in centre_cols:
        for r in range(board.rows):
            if g[r][c] == Cell.AI:
                score += 3    # Small bonus per AI piece in the centre
            elif g[r][c] == Cell.HUMAN:
                score -= 3    # Penalise Human presence in the centre

    # ── 2. Horizontal Windows ─────────────────────────────────────────────
    for r in range(board.rows):
        for c in range(board.cols - CONNECT_N + 1):
            window = [g[r][c + i] for i in range(CONNECT_N)]
            score += _score_window(window)

    # ── 3. Vertical Windows ──────────────────────────────────────────────
    for r in range(board.rows - CONNECT_N + 1):
        for c in range(board.cols):
            window = [g[r + i][c] for i in range(CONNECT_N)]
            score += _score_window(window)

    # ── 4. Diagonal Windows (\ direction) ────────────────────────────────
    for r in range(board.rows - CONNECT_N + 1):
        for c in range(board.cols - CONNECT_N + 1):
            window = [g[r + i][c + i] for i in range(CONNECT_N)]
            score += _score_window(window)

    # ── 5. Diagonal Windows (/ direction) ────────────────────────────────
    for r in range(CONNECT_N - 1, board.rows):
        for c in range(board.cols - CONNECT_N + 1):
            window = [g[r - i][c + i] for i in range(CONNECT_N)]
            score += _score_window(window)

    return score
