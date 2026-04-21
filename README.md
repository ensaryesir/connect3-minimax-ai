# Connect-3 — Minimax AI Agent

An intelligent Connect-3 game agent built with Python, powered by the **Minimax algorithm** with **Alpha-Beta pruning** and a custom **window-based heuristic evaluation function**.

---

## Table of Contents

- [Overview](#overview)
- [Game Rules](#game-rules)
- [AI Architecture](#ai-architecture)
- [Heuristic Evaluation Function](#heuristic-evaluation-function)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Usage Examples](#usage-examples)
- [Technical Details](#technical-details)

---

## Overview

This project implements a terminal-based **Connect-3** game where a human player competes against an AI opponent. The AI uses the **Minimax** decision algorithm — the foundational algorithm for adversarial search in two-player zero-sum games — enhanced with **Alpha-Beta pruning** to dramatically reduce the search space.

When the search reaches its depth limit, a **window-based heuristic evaluation function** estimates the desirability of the board position by scanning every possible 3-cell alignment on the board.

## Game Rules

| Parameter      | Value                        |
|----------------|------------------------------|
| Board size     | 5 rows × 6 columns          |
| Win condition  | Connect **3** in a row       |
| Directions     | Horizontal, Vertical, Diagonal (both) |
| Gravity        | Pieces drop to the lowest available cell |
| Player 1       | Human (`X` — Cyan)           |
| Player 2       | AI (`O` — Red)               |

## AI Architecture

### Minimax Algorithm

The AI models the game as a **game tree** where:
- The **Maximizing player** (AI) picks moves that lead to the highest score.
- The **Minimizing player** (Human) picks moves that lead to the lowest score.
- **Terminal nodes** (win/loss/draw) return exact scores.
- **Non-terminal leaf nodes** (at depth limit) return heuristic estimates.

### Alpha-Beta Pruning

Alpha-Beta pruning eliminates branches that cannot influence the final decision:

- **Alpha (α)**: Best score the Maximizer is guaranteed — starts at −∞
- **Beta (β)**: Best score the Minimizer is guaranteed — starts at +∞
- **Pruning condition**: If α ≥ β at any node, skip remaining children

This optimization can reduce the effective branching factor from **b** to approximately **√b**, allowing deeper searches within the same time budget.

### Depth-Limited Search

A configurable depth limit (default: **5**) caps the search to keep computation practical. The AI typically evaluates **hundreds to thousands of nodes** per move in well under a second.

## Heuristic Evaluation Function

The board is scanned for every possible **window** (contiguous group) of 3 cells — horizontally, vertically, and diagonally. Each window is scored:

| Window Composition              | Score  |
|---------------------------------|--------|
| 3 AI pieces (win)               | +100   |
| 2 AI + 1 empty (threat to win)  | +10    |
| 1 AI + 2 empty (potential)      | +1     |
| 3 Human pieces (loss)           | −100   |
| 2 Human + 1 empty (danger)      | −10    |
| Mixed (AI + Human)              | 0      |

**Center-column bonus**: Pieces in the center column(s) receive an additional ±3 weight, encouraging the AI to control the board's strategic center where more alignment opportunities exist.

## Project Structure

The project code is divided into modular components according to software engineering principles:

```
connect3-minimax-ai/
├── src/
│   ├── __init__.py      # Makes 'src' a package
│   ├── constants.py     # Cell Enum, dimensions, depth settings
│   ├── board.py         # Board dataclass and game state logic
│   ├── heuristic.py     # Evaluation functions and scoring tables
│   ├── ai.py            # Minimax algorithm, search stats, AIAgent
│   └── game.py          # Main game loop, turn management, console UI
├── main.py              # Root script to start the application
└── README.md            # This file
```

## How to Run

### Prerequisites

- **Python 3.10+** (uses modern type hints and dataclasses)
- No external dependencies — standard library only

### Quick Start

```bash
# Run with default AI depth (5)
python main.py

# Run with custom AI depth (e.g., depth 7 for stronger play)
python main.py 7
```

## Usage Examples

### Gameplay

```
==================================================
         CONNECT-3  ·  Minimax AI Agent
==================================================
  Board : 5 rows × 6 columns
  AI Depth : 5  |  Win : 3 in a row
  Human : X  |  AI : O
──────────────────────────────────────────────────
  1   2   3   4   5   6
┌───┬───┬───┬───┬───┬───┐
│ · │ · │ · │ · │ · │ · │
├───┼───┼───┼───┼───┼───┤
│ · │ · │ · │ · │ · │ · │
├───┼───┼───┼───┼───┼───┤
│ · │ · │ · │ · │ · │ · │
├───┼───┼───┼───┼───┼───┤
│ · │ · │ · │ · │ · │ · │
├───┼───┼───┼───┼───┼───┤
│ · │ · │ · │ · │ · │ · │
└───┴───┴───┴───┴───┴───┘

[YOUR TURN] Choose a column (1–6): 3
```

### AI Performance Statistics

After each AI move, the game displays:
```
[AI THINKING...] Done!
  → AI dropped O into column 4.
  ┌─ Search Stats ─────────────────────────────┐
  │  Time elapsed : 0.0594 seconds              │
  │  Nodes explored : 841                       │
  │  Branches pruned : 147                      │
  └────────────────────────────────────────────┘
```

## Technical Details

### Complexity Analysis

| Metric                  | Without Pruning     | With Alpha-Beta   |
|-------------------------|---------------------|--------------------|
| Branching factor        | b = 6               | ≈ √6 ≈ 2.45       |
| Nodes at depth d        | O(b^d) = O(6^5)     | O(b^(d/2)) ≈ O(6^2.5) |
| Approximate nodes (d=5) | ~7,776              | ~500–1,500         |

### Design Decisions

1. **Modular Architecture** — The application logic is logically separated to promote code readability and scalability.
2. **In-place move/undo** — Instead of copying the board at each tree level, the AI drops a piece, recurses, then removes it. This drastically reduces memory allocation overhead.
3. **Depth bonus for terminal states** — Win scores include `+depth` so the AI prefers faster wins and slower losses in branching alternatives.
4. **UTF-8 stdout reconfiguration** — Automatically handles Windows terminals with legacy codepages (e.g., cp1254 in Turkish environments) to flawlessly render Unicode line drawings.

