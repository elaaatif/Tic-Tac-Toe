import tkinter as tk
from tkinter import messagebox
import random

# Constants for player symbols
X = "X"
O = "O"
EMPTY = " "

class TicTacToe:
    def __init__(self, player_symbol):
        self.board = [EMPTY] * 9
        self.current_player = player_symbol
        self.game_over = False

    def apply_move(self, move):
        if not self.game_over and self.board[move] == EMPTY:
            self.board[move] = self.current_player
            if self.is_winner():
                self.game_over = True
            elif self.is_board_full():
                self.game_over = True
            else:
                self.toggle_player()

    def toggle_player(self):
        self.current_player = O if self.current_player == X else X

    def is_winner(self):
        # Check for a winner
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            if (
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                and self.board[combo[0]] != EMPTY
            ):
                return True
        return False

    def is_board_full(self):
        return all(cell != EMPTY for cell in self.board)

    def get_empty_cells(self):
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def minimax(self, depth, maximizing_player):
        if self.is_winner():
            return -1 if maximizing_player else 1
        elif self.is_board_full():
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_empty_cells():
                self.apply_move(move)
                eval = self.minimax(depth + 1, False)
                self.board[move] = EMPTY
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_empty_cells():
                self.apply_move(move)
                eval = self.minimax(depth + 1, True)
                self.board[move] = EMPTY
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self):
        best_score = float('-inf')
        best_move = None
        for move in self.get_empty_cells():
            self.apply_move(move)
            score = self.minimax(0, False)
            self.board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

def make_computer_move(game):
    move = game.best_move()
    game.apply_move(move)

def update_board_labels():
    for i in range(9):
        if game.board[i] == X:
            board_labels[i].config(text="X", bg="#3498db", fg="white")
        elif game.board[i] == O:
            board_labels[i].config(text="O", bg="#e74c3c", fg="white")
        else:
            board_labels[i].config(text="", bg="#ecf0f1")

def player_move(move):
    game.apply_move(move)
    update_board_labels()
    if game.is_winner():
        if game.current_player == X:
            messagebox.showinfo("Game Over", "Congratulations! You won!")
        else:
            messagebox.showinfo("Game Over", "Sorry, you lost.")
        reset_game()
    elif game.is_board_full():
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_game()
    else:
        make_computer_move(game)
        update_board_labels()
        if game.is_winner():
            if game.current_player == X:
                messagebox.showinfo("Game Over", "Congratulations! You won!")
            else:
                messagebox.showinfo("Game Over", "Sorry, you lost.")
            reset_game()
        elif game.is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()

def reset_game():
    game.board = [EMPTY] * 9
    game.game_over = False
    update_board_labels()

def choose_symbol():
    symbol_choice = tk.StringVar()
    symbol_choice.set(X)  # Default selection

    def set_player_symbol():
        player_symbol = symbol_choice.get()
        game.current_player = player_symbol
        reset_game()

    tk.Label(app, text="Choose Your Symbol:", font=("Helvetica", 12), bg="#2c3e50", fg="white").grid(row=12, column=0, columnspan=3)

    tk.Radiobutton(app, text="X", variable=symbol_choice, value=X, command=set_player_symbol, font=("Helvetica", 10),
                   bg="#3498db", fg="white").grid(row=13, column=0, pady=5, padx=10)
    tk.Radiobutton(app, text="O", variable=symbol_choice, value=O, command=set_player_symbol, font=("Helvetica", 10),
                   bg="#e74c3c", fg="white").grid(row=13, column=1, pady=5, padx=10)

# GUI Setup
app = tk.Tk()
app.title("Tic Tac Toe")
app.configure(bg="#2c3e50")

# Add two labels on top of the Tic Tac Toe grid
tk.Label(app, text="Tic Tac Toe FOR FUN", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white").grid(row=0, column=0, columnspan=3, pady=10)
tk.Label(app, text="MADE AS AI TP", font=("Helvetica", 12), bg="#2c3e50", fg="white").grid(row=1, column=0, columnspan=3, pady=5)

choose_symbol()

game = TicTacToe(X)

# Create GUI labels for the Tic Tac Toe board and associate them with the player_move function
board_labels = []
for i in range(9):
    label = tk.Label(app, bg="#ecf0f1", width=8, height=4, font=("Helvetica", 16, "bold"))
    label.grid(row=i // 3 + 2, column=i % 3, padx=5, pady=5)
    label.bind("<Button-1>", lambda event, move=i: player_move(move))
    board_labels.append(label)

# Add a "Reset Game" button to reset the game
tk.Button(app, text="Reset Game", command=reset_game, font=("Helvetica", 12), bg="#2ecc71", fg="white").grid(row=11, column=0, columnspan=3, pady=10)

# Run the Tkinter main loop
app.mainloop()
