import os
import sys

from .constants import Cell, CONNECT_N, DEFAULT_DEPTH
from .board import Board
from .ai import AIAgent

class Game:
    """Orchestrates the Connect-3 game."""

    def __init__(self, ai_depth: int = DEFAULT_DEPTH) -> None:
        self.board = Board()
        self.ai = AIAgent(depth=ai_depth)
        self.current_player: Cell = Cell.HUMAN

    @staticmethod
    def clear_screen() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self) -> None:
        print("\033[1;93m" + "=" * 50)
        print("         CONNECT-3  ·  Minimax AI Agent")
        print("=" * 50 + "\033[0m")
        print(f"  Board : {self.board.rows} rows × {self.board.cols} columns")
        print(f"  AI Depth : {self.ai.depth}  |  Win : {CONNECT_N} in a row")
        print(f"  Human : \033[96mX\033[0m  |  AI : \033[91mO\033[0m")
        print("─" * 50)

    def human_turn(self) -> None:
        valid_cols = self.board.get_valid_columns()

        while True:
            try:
                raw = input(
                    f"\n\033[96m[YOUR TURN]\033[0m Choose a column "
                    f"(1–{self.board.cols}): "
                )
                col = int(raw) - 1

                if col not in valid_cols:
                    print(
                        f"  ⚠  Invalid choice. "
                        f"Available columns: "
                        f"{[c + 1 for c in valid_cols]}"
                    )
                    continue
                break
            except ValueError:
                print("  ⚠  Please enter a valid integer.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nGame aborted. Goodbye!")
                sys.exit(0)

        self.board.drop_piece(col, Cell.HUMAN)
        print(f"  → You dropped \033[96mX\033[0m into column {col + 1}.")

    def ai_turn(self) -> None:
        print(f"\n\033[91m[AI THINKING...]\033[0m", end=" ", flush=True)

        best_col, elapsed, stats = self.ai.choose_move(self.board)
        self.board.drop_piece(best_col, Cell.AI)

        print(f"Done!")
        print(f"  → AI dropped \033[91mO\033[0m into column {best_col + 1}.")
        print(f"  ┌─ Search Stats ─────────────────────────────┐")
        print(f"  │  Time elapsed : {elapsed:.4f} seconds{' ' * max(0, 14 - len(f'{elapsed:.4f}'))}│")
        print(f"  │  Nodes explored : {stats.nodes_explored:,}{' ' * max(0, 12 - len(f'{stats.nodes_explored:,}'))}│")
        print(f"  │  Branches pruned : {stats.nodes_pruned:,}{' ' * max(0, 11 - len(f'{stats.nodes_pruned:,}'))}│")
        print(f"  └────────────────────────────────────────────┘")

    def play(self) -> None:
        self.clear_screen()
        self.print_banner()
        self.board.display()

        while True:
            if self.current_player == Cell.HUMAN:
                self.human_turn()
            else:
                self.ai_turn()

            print()
            self.board.display()

            if self.board.check_winner(self.current_player):
                if self.current_player == Cell.HUMAN:
                    print("\n\033[1;92m🎉 Congratulations! You win!\033[0m\n")
                else:
                    print("\n\033[1;91m🤖 The AI wins! Better luck next time.\033[0m\n")
                break

            if self.board.is_full():
                print("\n\033[1;93m🤝 It's a draw! The board is full.\033[0m\n")
                break

            self.current_player = (
                Cell.AI if self.current_player == Cell.HUMAN else Cell.HUMAN
            )
