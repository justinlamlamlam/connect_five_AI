class Board:
    def __init__(self):
        self.rows = 7
        self.cols = 9
        self.connect = 5
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1  # Track who's turn it is

    def print_board(self):
        print("\nCurrent Board:")
        for row in self.grid:
            print(" | " + " | ".join(str(cell) if cell != 0 else " " for cell in row) + " |")
        print("   " + "   ".join(str(i+1) for i in range(self.cols)) + "\n")

    def make_move(self, col: int, player: int):
        if col < 1 or col > self.cols:
            print(f"Invalid column: {col}. Choose between 1 and {self.cols}.")
            return None

        col -= 1
        for row in reversed(range(self.rows)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                self.current_player = player 
                return row  # Return row of the move
        print(f"Column {col + 1} is full.")
        return None
    
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
    
    def check_winner(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row in range(self.rows):
            for col in range(self.cols):
                player = self.grid[row][col]
                if player == 0:
                    continue
                for dr, dc in directions:
                    count = 1
                    r, c = row + dr, col + dc
                    while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == player:
                        count += 1
                        if count == self.connect:
                            return player
                        r += dr
                        c += dc
        return None