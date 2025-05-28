# play.py

import tkinter as tk
import connect5
import mcts
import copy

PLAYER_HUMAN = 1
PLAYER_AI = 2

class Connect5GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 5")

        self.canvas = tk.Canvas(root, width=630, height=490, bg="blue")
        self.canvas.pack()

        self.board = connect5.create_board()
        self.turn = None  # تعیین میشه بعد از انتخاب دکمه
        self.game_over = False

        self.canvas.bind("<Button-1>", self.click_event)

        self.start_frame = tk.Frame(root)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="چه کسی اول بازی کند؟").pack(side=tk.LEFT)

        tk.Button(self.start_frame, text="AI اول شروع کند", command=lambda: self.start_game(PLAYER_AI)).pack(side=tk.LEFT)
        tk.Button(self.start_frame, text="من اول شروع کنم", command=lambda: self.start_game(PLAYER_HUMAN)).pack(side=tk.LEFT)

        self.draw_board()

    def start_game(self, first_player):
        self.turn = first_player
        self.start_frame.destroy()
        if self.turn == PLAYER_AI:
            self.ai_move()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(connect5.ROWS):
            for col in range(connect5.COLS):
                x0 = col * 70 + 5
                y0 = row * 70 + 5
                x1 = x0 + 60
                y1 = y0 + 60
                val = self.board[row][col]
                color = "white"
                if val == PLAYER_HUMAN:
                    color = "red"
                elif val == PLAYER_AI:
                    color = "yellow"
                self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def click_event(self, event):
        if self.game_over or self.turn != PLAYER_HUMAN:
            return

        col = event.x // 70
        if connect5.is_valid_move(self.board, col):
            connect5.apply_move(self.board, col, PLAYER_HUMAN)
            self.draw_board()
            if connect5.check_win(self.board, PLAYER_HUMAN):
                self.end_game("🎉 شما بردید!")
                return
            if connect5.is_draw(self.board):
                self.end_game("بازی مساوی شد.")
                return
            self.turn = PLAYER_AI
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        col = mcts.mcts(copy.deepcopy(self.board), PLAYER_AI, iterations=400)
        connect5.apply_move(self.board, col, PLAYER_AI)
        self.draw_board()
        if connect5.check_win(self.board, PLAYER_AI):
            self.end_game("😈 کامپیوتر برد.")
        elif connect5.is_draw(self.board):
            self.end_game("بازی مساوی شد.")
        else:
            self.turn = PLAYER_HUMAN

    def end_game(self, message):
        self.game_over = True
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(315, 245, text=message, font=("Arial", 30), fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect5GUI(root)
    root.mainloop()
