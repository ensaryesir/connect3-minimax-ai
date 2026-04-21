import math
import time
from dataclasses import dataclass
from typing import Optional

from .constants import Cell, DEFAULT_DEPTH
from .board import Board
from .heuristic import evaluate_board


@dataclass
class SearchStats:
    """Track statistics about the Minimax search for display purposes."""
    nodes_explored: int = 0
    nodes_pruned: int = 0


def minimax(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    stats: SearchStats,
) -> tuple[float, Optional[int]]:
    """Minimax with Alpha-Beta Pruning."""
    stats.nodes_explored += 1

    valid_cols = board.get_valid_columns()

    if board.check_winner(Cell.AI):
        return (10_000 + depth, None)

    if board.check_winner(Cell.HUMAN):
        return (-10_000 - depth, None)

    if not valid_cols:
        return (0, None)  # Draw

    if depth == 0:
        return (evaluate_board(board), None)

    best_col: Optional[int] = valid_cols[0]

    if is_maximizing:
        max_eval = -math.inf
        for col in valid_cols:
            row = board.drop_piece(col, Cell.AI)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, stats)
            board.remove_piece(row, col)

            if eval_score > max_eval:
                max_eval = eval_score
                best_col = col

            alpha = max(alpha, eval_score)
            if alpha >= beta:
                stats.nodes_pruned += 1
                break
        return (max_eval, best_col)
    else:
        min_eval = math.inf
        for col in valid_cols:
            row = board.drop_piece(col, Cell.HUMAN)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, stats)
            board.remove_piece(row, col)

            if eval_score < min_eval:
                min_eval = eval_score
                best_col = col

            beta = min(beta, eval_score)
            if alpha >= beta:
                stats.nodes_pruned += 1
                break
        return (min_eval, best_col)


class AIAgent:
    """Wraps the Minimax search."""
    def __init__(self, depth: int = DEFAULT_DEPTH) -> None:
        self.depth = depth

    def choose_move(self, board: Board) -> tuple[int, float, SearchStats]:
        stats = SearchStats()
        start_time = time.perf_counter()

        _, best_col = minimax(
            board=board,
            depth=self.depth,
            alpha=-math.inf,
            beta=math.inf,
            is_maximizing=True,
            stats=stats,
        )

        elapsed = time.perf_counter() - start_time

        if best_col is None:
            best_col = board.get_valid_columns()[0]

        return best_col, elapsed, stats
