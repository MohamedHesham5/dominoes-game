import tkinter as tk
from tkinter import messagebox
import itertools 
import random
import re

class DominoesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dominoes Game")
        self.geometry("1000x700")  
        self.configure(bg="#f0f0f0")  

        self.game = Dominoes()
        self.prepare_game()

        self.create_widgets()

        self.after(100, self.game_loop)

    def prepare_game(self):
        self.game.get_domino_stock()
        self.game.get_domino_bricks()
        self.game.prepare_to_play()

    def create_widgets(self):
        
        self.label_turn = tk.Label(self, text="Player 1's Turn", font=("Arial", 18, "bold"), bg="#f0f0f0")
        self.label_turn.pack(pady=10)

        self.text_game_info = tk.Text(self, height=10, width=60, font=("Arial", 12), bg="#ffffff", relief=tk.SOLID, bd=2)
        self.text_game_info.pack(pady=10)

        self.label_player_pieces = tk.Label(self, text="Player 1 Pieces:", font=("Arial", 14), bg="#f0f0f0")
        self.label_player_pieces.pack(pady=5)

        self.entry_player_move = tk.Entry(self, font=("Arial", 12), relief=tk.SOLID, bd=2)
        self.entry_player_move.pack(pady=10)

        self.button_player_move = tk.Button(self, text="Make Move", command=self.player_move, font=("Arial", 12), bg="#4caf50", fg="#ffffff", relief=tk.RAISED, bd=2)
        self.button_player_move.pack(pady=10)

        self.label_player_pieces2 = tk.Label(self, text="Player 2 Pieces:", font=("Arial", 14), bg="#f0f0f0")
        self.label_player_pieces2.pack(pady=5)

        self.update_display()

    def game_loop(self):
        self.game.result_check()

        if self.game.status == 'player':
            self.label_turn.config(text="Player 1's turn")
            self.wait_for_player_input()
        elif self.game.status == 'player2':
            self.label_turn.config(text="Player 2's turn")
            self.wait_for_player2_input()
        elif self.game.status == 'draw':
            self.label_turn.config(text="Game Over - It's a draw!")
            self.button_player_move.config(state=tk.DISABLED)
            winner = self.game.determine_winner() 

        self.after(100, self.game_loop)

    def wait_for_player_input(self):
        self.button_player_move.config(state=tk.NORMAL)
        self.entry_player_move.bind("<Return>", self.player_move)

    def wait_for_player2_input(self):
        self.button_player_move.config(state=tk.DISABLED)
        self.after(1000, self.player2_move_ai)

    def player_move(self, event=None):
        user_input = self.entry_player_move.get()

        result = self.game.player_move(user_input)
        if result == -1:
        
            messagebox.showwarning("Invalid Move", "Invalid move. Please try again.")
        else:
            self.update_display()

            if self.game.status == 'player2':
                # If it's now Player 2's turn, wait for their input
                self.wait_for_player2_input()

    def player2_move_ai(self):
    # AI makes a move
     if self.game.status == 'player2':
        if self.game.player2_pieces:  # Check if player 2 has pieces
            matching_pieces = [i for i, piece in enumerate(self.game.player2_pieces) if piece[0] in self.game.domino_snake[0] or piece[1] in self.game.domino_snake[0]]
            if matching_pieces:
                random_move = random.choice(matching_pieces)
                self.game.player2_move(str(random_move + 1))  # Indexes are 1-based in UI
            else:
                # If player 2 has no matching pieces, draw a new piece
                drawn_piece = self.game.stock_pieces.pop(random.randint(0, len(self.game.stock_pieces)-1))
                self.game.player2_pieces.append(drawn_piece)
                self.game.status = 'player'
        else:
            # If player 2 has no pieces, draw a new piece
              drawn_piece = self.game.stock_pieces.pop(random.randint(0, len(self.game.stock_pieces)-1))
              self.game.player2_pieces.append(drawn_piece)
              self.game.status = 'player'

        self.update_display()

            
        available_moves = [f'{i+1}' for i in range(len(self.game.player2_pieces))]
        random_move = random.choice(available_moves)
        self.game.player2_move(random_move)
        self.update_display()

        if self.game.status == 'player':
                                # If it's now Player 1's turn, wait for their input
                self.wait_for_player_input()
            
        else:
            # If player 2 has no pieces, draw a new piece
            self.game.player2_pieces.append(self.game.stock_pieces.pop(random.randint(0, len(self.game.stock_pieces)-1)))
            self.game.status = 'player'
            
            self.update_display()
            self.wait_for_player_input()  # Wait for player 1 input

    def update_display(self):
        game_info = f"Stock size(num of currently dominoes pieces): {len(self.game.stock_pieces)}\n"
        game_info += f"Domino Snake (Board): {self.game.domino_snake}\n"

        self.text_game_info.delete("1.0", tk.END)  # Clear the Text widget
        self.text_game_info.insert(tk.END, game_info)

        self.entry_player_move.delete(0, tk.END)  # Clear the entry field

        self.label_player_pieces.config(text=f"Player 1 pieces: {self.game.player_pieces}")
        self.label_player_pieces2.config(text=f"Player 2 pieces: {self.game.player2_pieces}")

        if self.game.status == 'player':
            # Enable player move button for the current player's turn
            self.button_player_move.config(state=tk.NORMAL)
        elif self.game.status == 'player2':
            # Disable player move button while the AI is making a move
            self.button_player_move.config(state=tk.DISABLED)
        else:
            # Disable player move button while the other player is making a move
            self.button_player_move.config(state=tk.DISABLED)


class Dominoes:
    def __init__(self):
        self.stock_pieces = []
        self.player_pieces = []
        self.player2_pieces = []
        self.domino_snake = []
        self.status = 'player'

    def get_domino_stock(self):
        stock = list(itertools.combinations(range(7), 2))
        for i in range(7):
            stock.append((i, i))
        self.stock_pieces = list(map(list, stock))

    def get_domino_bricks(self):
        for _ in range(7):
            self.player_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))
            self.player2_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))

    def prepare_to_play(self):
        return 1

    def player_move(self, request):
     pattern = r'^-?\d+$'  # Updated regex to accept any integer input
     if re.match(pattern, request) is None:
        return -1
     req = int(request)
     if abs(req) > len(self.player_pieces):
        return -1
     elif req > 0:
        if self.add_piece_to_snake(req - 1, 'right') == -1:
            return -1
     elif req < 0:
        if self.add_piece_to_snake(-req - 1, 'left') == -1:
            return -1
     else:
        drawn_piece = self.stock_pieces.pop(random.randint(0, len(self.stock_pieces) - 1))
        self.player_pieces.append(drawn_piece)
     self.status = 'player2'


    def player2_move(self, request):
        pattern = r'^-?[0-7]$'
        if re.match(pattern, request) is None:
            return -1
        req = list(request)
        if len(req) > 1:
            if int(req[1]) > len(self.player2_pieces):
                return -1
            elif self.add_piece_to_snake(int(req[1]) - 1, 'left') == -1:
                return -1
        elif int(req[0]) > 0:
            if int(req[0]) > len(self.player2_pieces):
                return -1
            elif self.add_piece_to_snake(int(req[0]) - 1, 'right') == -1:
                return -1
        else:
            drawn_piece = self.stock_pieces.pop(random.randint(0, len(self.stock_pieces) - 1))
            self.player2_pieces.append(drawn_piece)
        self.status = 'player'

    def add_piece_to_snake(self, piece_no, snake_side):
        if self.status == 'player':
            player_pieces = self.player_pieces
        elif self.status == 'player2':
            player_pieces = self.player2_pieces
        else:
            assert False, "add_piece_to_snake Wrong status"

        if snake_side == 'left' :

            if self.domino_snake:
                # If domino_snake is not empty, check if the selected piece can be added to the left
                if self.domino_snake[0][0] not in player_pieces[piece_no]:
                    return -1
                elif self.domino_snake[0][0] == player_pieces[piece_no][0]:
                    player_pieces[piece_no].reverse()
                    self.domino_snake.insert(0, player_pieces.pop(piece_no))
                elif self.domino_snake[0][0] == player_pieces[piece_no][1]:
                    self.domino_snake.insert(0, player_pieces.pop(piece_no))
                else:
                    return -1
            else:
                # If domino_snake is empty, add the piece to the left without checking
                self.domino_snake.insert(0, player_pieces.pop(piece_no))
        elif snake_side == 'right':
            if self.domino_snake:
                # If domino_snake is not empty, check if the selected piece can be added to the right
                if self.domino_snake[-1][-1] not in player_pieces[piece_no]:
                    return -1
                elif self.domino_snake[-1][-1] == player_pieces[piece_no][0]:
                    self.domino_snake.append(player_pieces.pop(piece_no))
                elif self.domino_snake[-1][-1] == player_pieces[piece_no][1]:
                    player_pieces[piece_no].reverse()
                    self.domino_snake.append(player_pieces.pop(piece_no))
                else:
                    return -1
            else:
                # If domino_snake is empty, add the piece to the right without checking
                self.domino_snake.append(player_pieces.pop(piece_no))

    def result_check(self):
        if len(self.player_pieces) == 0:
            self.status = 'player'
            print("THE PLAYER IS WIN") 
            messagebox.showinfo("Game Over", "Player is Win!")

        elif len(self.player2_pieces) == 0:
            self.status = 'player2'
            print("AI IS WIN")
            messagebox.showinfo("Game Over", "AI Wins!")
            self.button_player_move.config(state=tk.DISABLED)

        elif len(self.stock_pieces) == -1:
            self.status = 'draw'

    def determine_winner(self):
        if self.status == 'player':
            return "AI"
        elif self.status == 'player2':
            return "Player "
        else:
            return "No one"


if __name__ == "__main__":
    app = DominoesGUI()
    app.mainloop()
