"""
Global configuration for Minesweeper game.
"""

# Default board size and mine count
DEFAULT_ROWS = 9
DEFAULT_COLS = 9
DEFAULT_MINES = 10

# Difficulty presets: key -> (Name, rows, cols, mines)
DIFFICULTIES = {
    '1': ('Beginner',     9,  9,  10),
    '2': ('Intermediate', 16, 16, 40),
    '3': ('Expert',       30, 16, 99),
}

# Skill definitions: name -> (description, max uses)
SKILLS = {
    'eliminate': ('Remove a mine or reveal a safe spot', 3),
    'revive':    ('Automatically revive once when hitting a mine', 1),
}

# Display symbols
HIDDEN = '■'       # unrevealed cell
FLAG   = '⚑'       # flagged cell
MINE   = 'M'       # mine cell
