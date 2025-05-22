import tkinter as tk
from tkinter import messagebox
from game_logic import MinesweeperGame
from shape_generator import random_shape
import config


def launch_selector():
    selector = tk.Tk()
    selector.title("select model")
    tk.Label(selector, text="Select Difficulty or Random Map:").pack(padx=10, pady=5)
    mode_var = tk.StringVar(value='1')
    for key, (name, r, c, m) in config.DIFFICULTIES.items():
        tk.Radiobutton(
            selector,
            text=f"{key}. {name} ({r}×{c}, {m} mines)",
            variable=mode_var,
            value=key
        ).pack(anchor='w')
    tk.Button(
        selector,
        text="Random map",
        command=lambda: start_game(None, selector)
    ).pack(fill='x', padx=10, pady=5)
    tk.Button(
        selector,
        text="START",
        command=lambda: start_game(mode_var.get(), selector)
    ).pack(fill='x', padx=10, pady=5)
    selector.mainloop()


def start_game(choice, parent):
    parent.destroy()
    if choice in config.DIFFICULTIES:
        _, rows, cols, mines = config.DIFFICULTIES[choice]
        shape = [['.' for _ in range(cols)] for _ in range(rows)]
        show_skills = True
    else:
        cols, rows = 30, 16
        raw = random_shape(cols, rows)
        playable = [(r, c) for r, row in enumerate(raw) for c, ch in enumerate(row) if ch == '.']
        mines = max(config.DEFAULT_MINES, int(len(playable) * 0.2))
        shape = raw
        show_skills = False  
    launch_game_gui(rows, cols, mines, shape, show_skills)


def launch_game_gui(rows, cols, mines, shape, show_skills=True):
    game = MinesweeperGame(shape, mines)
    root = tk.Tk()
    root.title("minesweeper GUI")

    buttons = {}
    skill_buttons = {}

    def restart():
        root.destroy()
        launch_selector()

    def reveal_all():
        for (r, c), btn in buttons.items():
            if shape[r][c] == '#':
                continue
            if game.board[(r, c)] == config.MINE:
                btn.config(text='M', bg='red')

    def use_skill(name):
        if not game.use_skill(name):
            messagebox.showwarning("ability", f"there is no {name}")
        refresh()

    def on_left(r, c):
        if shape[r][c] == '#' or game.game_over:
            return
        game.reveal(r, c)
        refresh()
        if game.game_over:
            reveal_all()
            messagebox.showinfo("Game Over", "BOOM! Game over！")
            restart()
        elif game.check_win():
            reveal_all()
            messagebox.showinfo("Victory", "congradulation！")
            restart()

    def on_right(event, r, c):
        if not show_skills:
            return  # random
        if shape[r][c] == '#' or game.game_over:
            return
        game.toggle_flag(r, c)
        refresh()

    def refresh():
        for (r, c), btn in buttons.items():
            if shape[r][c] == '#':
                btn.config(bg='white', state='disabled', relief=tk.FLAT)
            else:
                pos = (r, c)
                if game.visible[pos]:
                    val = game.board[pos]
                    btn.config(text='' if val == 0 else str(val), bg='lightgrey', state='disabled')
                elif show_skills and game.flags[pos]:
                    btn.config(text='⚑', fg='red', bg='black')
                else:
                    btn.config(text='', bg='navy', state='normal', relief=tk.RAISED)
        remaining = sum(1 for pos, val in game.board.items() if val == config.MINE and not game.flags[pos])
        bombs_var.set(f"Remaining mines: {remaining}")
        for name, btn in skill_buttons.items():
            btn.config(text=f"{name} ({game.skills.get(name, 0)})")

    # create button
    board_frame = tk.Frame(root)
    board_frame.grid(row=0, column=0)
    for r in range(rows):
        for c in range(cols):
            btn = tk.Button(
                board_frame,
                width=2,
                height=1,
                command=lambda r=r, c=c: on_left(r, c),
                bg='black'  
            )
            btn.grid(row=r, column=c)
            if show_skills:
                btn.bind('<Button-3>', lambda e, r=r, c=c: on_right(e, r, c))
                btn.bind('<Button-2>', lambda e, r=r, c=c: on_right(e, r, c))
            buttons[(r, c)] = btn

    # right side of dashboard
    panel = tk.Frame(root)
    panel.grid(row=0, column=1, sticky='ns', padx=10, pady=5)
    if show_skills:
        tk.Label(panel, text="ability").pack(pady=5)
        for name, (desc, _) in config.SKILLS.items():
            btn = tk.Button(
                panel,
                text=f"{name} ({game.skills.get(name, 0)})",
                width=12,
                command=lambda n=name: use_skill(n)
            )
            btn.pack(pady=2)
            skill_buttons[name] = btn
            tk.Label(panel, text=desc).pack()
    bombs_var = tk.StringVar()
    tk.Label(panel, textvariable=bombs_var).pack(pady=10)
    tk.Button(panel, text="Display of all mines", command=reveal_all).pack(fill='x', pady=5)

    refresh()
    root.mainloop()

if __name__ == '__main__':
    launch_selector()
