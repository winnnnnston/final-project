import random
from config import MINE, SKILLS

class MinesweeperGame:
    """
    Core game logic for arbitrary-shaped Minesweeper.

    Manages mine placement, revealing, flagging, skills, and win/loss.
    """
    def __init__(self, shape_mask, mines):
        # shape_mask: 2D list of '#' (wall) and '.' (playable)
        self.shape    = shape_mask
        # List of all playable positions
        self.playable = [(r, c)
                         for r, row in enumerate(shape_mask)
                         for c, ch in enumerate(row) if ch == '.']
        self.rows     = len(shape_mask)
        self.cols     = max(len(row) for row in shape_mask)
        self.mines    = min(mines, len(self.playable))

        # Tracking board state
        self.board    = {pos:0     for pos in self.playable}  # 0-8 or MINE
        self.visible  = {pos:False for pos in self.playable}  # revealed?
        self.flags    = {pos:False for pos in self.playable}  # flagged?

        # Skills usage remaining
        self.skills   = {name:cnt for name,(_,cnt) in SKILLS.items()}

        # Place mines and calculate neighbor counts
        self._place_mines()
        self._compute_counts()

        self.revealed  = 0
        self.game_over = False

    def _place_mines(self):
        # Randomly place mines on playable cells
        for pos in random.sample(self.playable, self.mines):
            self.board[pos] = MINE

    def _compute_counts(self):
        # Calculate number of adjacent mines for each cell
        for r, c in self.playable:
            if self.board[(r, c)] == MINE:
                continue
            count = 0
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    nbr = (r+dr, c+dc)
                    if nbr in self.board and self.board[nbr] == MINE:
                        count += 1
            self.board[(r, c)] = count

    def neighbors(self, pos):
        # Yield all valid neighbors of pos
        r, c = pos
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                nbr = (r+dr, c+dc)
                if nbr != pos and nbr in self.board:
                    yield nbr

    def reveal(self, r, c):
        """
        Reveal a cell. Uses flood-fill for zeros, handles revive skill if hitting a mine.
        """
        pos = (r, c)
        if self.game_over or self.flags[pos] or self.visible[pos]:
            return
        if self.board[pos] == MINE:
            # Use revive skill if available
            if self.skills.get('revive', 0) > 0:
                self.skills['revive'] -= 1
                self.board[pos] = 0
                self._flood_fill(pos)
            else:
                self.game_over = True
            return
        self._flood_fill(pos)

    def _flood_fill(self, start):
        # Iterative flood-fill to reveal all connected zero regions
        stack = [start]
        while stack:
            pos = stack.pop()
            if self.visible[pos]:
                continue
            self.visible[pos] = True
            self.revealed += 1
            if self.board[pos] == 0:
                for nbr in self.neighbors(pos):
                    if not self.visible[nbr] and not self.flags[nbr]:
                        stack.append(nbr)

    def toggle_flag(self, r, c):
        """Place or remove a flag on a cell."""
        pos = (r, c)
        if self.game_over or self.visible[pos]:
            return
        self.flags[pos] = not self.flags[pos]

    def check_win(self):
        """Return True if the player has won."""
        # Win if all non-mine cells are revealed
        if self.revealed == len(self.playable) - self.mines:
            return True
        # Or if all mines are flagged correctly
        correct = sum(1 for pos in self.playable
                      if self.board[pos] == MINE and self.flags[pos])
        return (correct == self.mines)

    def use_skill(self, name):
        """Use a skill: 'eliminate' or others."""
        if name not in self.skills or self.skills[name] <= 0:
            return False
        self.skills[name] -= 1
        if name == 'eliminate':
            # Randomly remove or reveal
            candidates = [p for p in self.playable if not self.visible[p] and not self.flags[p]]
            if not candidates:
                return False
            pos = random.choice(candidates)
            if self.board[pos] == MINE:
                self.board[pos] = 0
            self._flood_fill(pos)
            return True
        return True
