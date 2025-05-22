import os
from config import HIDDEN, FLAG, MINE, SKILLS


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_game(game):
    """Print the current game state to terminal."""
    clear_screen()
    # Column headers
    header = '   ' + ' '.join(f"{c:2}" for c in range(game.cols))
    print(header)
    # Each row
    for r, row in enumerate(game.shape):
        line = f"{r:2} "
        for c, ch in enumerate(row):
            if ch == '#':
                line += '   '
            else:
                pos = (r, c)
                if game.game_over and game.board[pos] == MINE:
                    sym = MINE
                elif game.flags[pos]:
                    sym = FLAG
                elif not game.visible[pos]:
                    sym = HIDDEN
                else:
                    sym = str(game.board[pos])
                line += f" {sym}"
        print(line)
    # Mine/Flag counts
    used_flags = sum(v for v in game.flags.values())
    print(f"Mines: {game.mines}   Flags: {used_flags}")
    # Skills
    print("Skills:")
    for name, (desc, _) in SKILLS.items():
        print(f"  {name}: {desc} (remaining {game.skills.get(name,0)})")


def prompt_move():
    """Prompt the user for their next move and return tokens."""
    return input("Enter: r x y to reveal, f x y to flag, s name to use skill > ").split()


def show_result(game):
    """Display final win/loss message."""
    if game.check_win():
        print("🎉 You win! Congratulations!")
    else:
        print("💥 You hit a mine. Game over.")

