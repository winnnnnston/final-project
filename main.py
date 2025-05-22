from config import DIFFICULTIES, DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES
from shape_generator import random_shape
from game_logic import MinesweeperGame
from ui import display_game, prompt_move, show_result


def main():
    # Mode selection
    print("Select mode:")
    print(" 1. Preset difficulty")
    print(" 2. Random cave map")
    mode = input("Enter 1 or 2: ").strip()

    if mode == '1':
        # Difficulty preset
        print("Choose difficulty:")
        for k, (name, r, c, m) in DIFFICULTIES.items():
            print(f" {k}. {name} ({r}×{c}, {m} mines)")
        choice = input("Enter 1-3: ").strip()
        if choice in DIFFICULTIES:
            _, rows, cols, mines = DIFFICULTIES[choice]
        else:
            print("Invalid choice. Using default 9×9×10.")
            rows, cols, mines = DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES
        shape = [['.' for _ in range(cols)] for _ in range(rows)]
    else:
        # Random cave
        cols, rows = 30, 16
        raw = random_shape(cols, rows)
        playable = [(r, c) for r, row in enumerate(raw) for c, ch in enumerate(row) if ch == '.']
        mines = max(DEFAULT_MINES, int(len(playable) * 0.2))
        shape = raw

    game = MinesweeperGame(shape, mines)
    # Main game loop
    while not game.game_over and not game.check_win():
        display_game(game)
        cmd = prompt_move()
        if not cmd:
            continue
        op = cmd[0]
        if op in ('r','f') and len(cmd)==3:
            try:
                x, y = map(int, cmd[1:3])
            except ValueError:
                print("Coordinates must be integers.")
                continue
            if x<0 or x>=game.rows or y<0 or y>=game.cols or game.shape[x][y]=='#':
                print("Invalid or blocked cell.")
                continue
            if op=='r':
                game.reveal(x,y)
            else:
                game.toggle_flag(x,y)
        elif op=='s' and len(cmd)==2:
            if not game.use_skill(cmd[1]):
                print(f"Skill '{cmd[1]}' unavailable or out of uses.")
        else:
            print("Invalid command. Use r x y, f x y, or s name.")

    display_game(game)
    show_result(game)

if __name__=='__main__':
    main()
