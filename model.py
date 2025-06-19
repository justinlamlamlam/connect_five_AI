from board import Board
from ai import RandomAI, MCTS_AI

class Game:
    def __init__(self, ai_player=2):
        self.board = Board()
        self.current_player = 1
        self.ai_player = ai_player
        # self.ai = RandomAI()
        self.ai = MCTS_AI(player=ai_player, simulations=1000)
        self.last_move = None  # Track last move for win checking

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def play_turn(self, col=None) -> bool:
        if self.current_player == self.ai_player:
            col = self.ai.choose_column(self.board)
            if col is None:
                print("AI cannot make a move. Game over.")
                return False
            print(f"AI chooses column {col}")
        elif col is None:
            print("Human player must provide a column.")
            return False

        row = self.board.make_move(col, self.current_player)
        if row is not None:
            self.last_move = (row, col - 1)
            self.board.print_board()
            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                exit()
            self.switch_player()
            return True

        return False

    def check_winner(self):
        if not self.last_move:
            return None
        row, col = self.last_move
        player = self.board.grid[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for sign in [1, -1]:
                r, c = row, col
                while True:
                    r += dr * sign
                    c += dc * sign
                    if 0 <= r < self.board.rows and 0 <= c < self.board.cols and self.board.grid[r][c] == player:
                        count += 1
                    else:
                        break
            if count >= self.board.connect:
                return player
        return None

    def is_ai_turn(self):
        return self.current_player == self.ai_player
