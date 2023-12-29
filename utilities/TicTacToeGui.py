import tkinter as tk
from tkinter import ttk
import random
import json

class TicTacToe:
    def __init__(self, initial_board=None):
        if initial_board is None:
            self.board = [' ' for _ in range(9)]  # Initialize an empty 3x3 grid
        else:
            # Verify that the provided initial_board is a valid 9-character string
            if len(initial_board) == 9 and all(char in ('X', 'O', ' ') for char in initial_board):
                self.board = list(initial_board)
            else:
                raise ValueError("Invalid initial board configuration")

        self.current_player = 'O'  # Start with player 'O'
        self.optimal_strategy = None
    def define_current_player(self,player) :
        self.current_player=player

    def get_board_config(self):
        return "".join(self.board)

    def set_board_from_config(self,config):
        for i in range(9):
            self.board[i]=config[i]
        return True

    def display_board(self):
        for i in range(3):
            for j in range(3):
                print(self.board[i * 3 + j], end="")

                if j < 2:
                    print(" | ", end="")

            print()  # Move to the next row
            if i < 2:
                print("---------")  # Display horizontal dividers between rows

    def get_all_possible_next_states(self,player):
        empty_cells = [i for i, char in enumerate(self.board) if char == ' ']
        next_states = []
        for cell in empty_cells:
            next_state = self.board.copy()
            next_state[cell] = player
            next_states.append("".join(next_state))
        return next_states

    def get_possible_moves(self):
        empty_cells=[]
        game,winner=self.is_game_over()
        if game!=True :
            for i in range(9):
                if self.board[i]==' ' :
                    empty_cells.append(i)
            return empty_cells
        return None
    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            # Toggle the current player for the next turn
            self.current_player = 'X' if self.current_player == 'O' else 'O'
            return True
        else:
            print("Invalid move. Try again. ")
            return False

    def is_game_over(self):
        # Check for win conditions
        # Check rows, columns, and diagonals for three in a row
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for condition in win_conditions:
            a, b, c = condition
            if (
                self.board[a] == self.board[b] == self.board[c] != ' '
            ):
                return True, self.board[a]

        # Check for a draw (no empty spaces left)
        if ' ' not in self.board:
            return True, None  # Game is a draw

        return False, None  # Game is not over yet
    def load_optimal_strategy(self, file_path):
        with open(file_path, 'r') as file:
            self.optimal_strategy = json.load(file)

    def make_computer_optimal_move(self):
        current_state = self.get_board_config()
        if current_state in self.optimal_strategy:
            optimal_move = self.optimal_strategy[current_state]
            if optimal_move is not None and self.board[optimal_move] == ' ':
                row, col = divmod(optimal_move, 3)
                self.make_move(row, col)
                return
        # If the current state is not in the optimal strategy or the optimal move is not valid, make a random move
        self.make_computer_move()
class TicTacToeGUI:
    def __init__(self, master, optimal_strategy_file):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 16), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 14), padding=10)

        self.style.configure('X.TButton', foreground='#e74c3c')  # Red for X
        self.style.configure('O.TButton', foreground='#2ecc71')  # Green for O

        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                button = ttk.Button(master, text="", style='TButton', width=6, command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=10)
                self.buttons[i][j] = button

        self.reset_button = ttk.Button(master, text="Reset", style='TButton', command=self.reset_game)
        self.reset_button.grid(row=3, column=1, pady=10)

        self.status_label = ttk.Label(master, text="", style='TLabel')
        self.status_label.grid(row=4, column=0, columnspan=3)
        self.master = master  # Store the reference to the master window
        # ... (rest of the __init__ method remains unchanged)
        self.game = TicTacToe()
        self.load_optimal_strategy(optimal_strategy_file)
        self.reset_game()

    def load_optimal_strategy(self, file_path):
        with open(file_path, 'r') as file:
            self.optimal_strategy = json.load(file)

     

    def make_move(self, row, col):
        if self.game.make_move(row * 3 + col):
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED)
            game_over, winner = self.game.is_game_over()
            if winner=='O':
                winner='X'
            elif winner=='X' :
                winner='O'
            if game_over:
                if winner:
                    self.update_status(f"Player {winner} wins!")
                else:
                    self.update_status("It's a draw!")

                # Disable all buttons after the game ends
                for i in range(3):
                    for j in range(3):
                        self.buttons[i][j].config(state=tk.DISABLED)

            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status()

                if self.current_player == 'O':
                    self.update_status("AI thinking...")
                    # Schedule the computer's move after a delay (in milliseconds)
                    self.master.after(1500, self.make_computer_optimal_move)

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)

        self.game = TicTacToe()
        self.current_player = 'X'
        self.update_status()
        
        if self.current_player == 'O':
            self.make_computer_optimal_move()
        
    def make_computer_optimal_move(self):
        current_state = self.game.get_board_config()
        optimal_move = self.optimal_strategy[current_state]
        print(optimal_move)
        if optimal_move is not None and self.game.board[optimal_move] == ' ':
            row, col = divmod(optimal_move, 3)
            self.make_move(row, col)
            return

        # If the current state is not in the optimal strategy or the optimal move is not valid, make a random move
        #self.make_computer_move()

    def make_computer_move(self):
        possible_moves = self.game.get_possible_moves()
        if possible_moves:
            random_move = random.choice(possible_moves)
            row, col = divmod(random_move, 3)
            self.make_move(row, col)

    def update_status(self, message=None):
        if message:
            self.reset_button.state(['!disabled'])
            self.status_label.config(text=message)
        else:
            self.status_label.config(text=f"Player {self.current_player}'s turn")
            style_name = 'X.TButton' if self.current_player == 'X' else 'O.TButton'
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].configure(style=style_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root, 'Optimal_strategy_DP.json')
    root.mainloop()


