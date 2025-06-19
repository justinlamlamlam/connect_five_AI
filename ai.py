import random
epsilon = 1e-6  # Small value to avoid division by zero in heuristics

class RandomAI:
    def choose_column(self, board):
        valid_columns = []
        for col in range(1, board.cols + 1):
            if board.grid[0][col - 1] == 0:
                valid_columns.append(col)
        return random.choice(valid_columns) if valid_columns else None
import math, random
from copy import deepcopy

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state              # Board object
        self.parent = parent
        self.move = move                # Column used to get here
        self.children = []
        self.visits = 0
        self.wins = 0

    def uct_score(self, exploration=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

class MCTS_AI:
    def __init__(self, player=2, simulations=1000):
        self.player = player
        self.simulations = simulations

    def choose_column(self, board):
        root = MCTSNode(state=deepcopy(board))
        for _ in range(self.simulations):
            node = self._select(root)
            result = self._simulate(node.state)
            self._backpropagate(node, result)

        # Prepare win rate report
        col_stats = ["x"] * board.cols
        for child in root.children:
            idx = child.move - 1
            if child.visits > 0:
                winrate = child.wins / child.visits
                col_stats[idx] = f"{winrate:.2f}"
            else:
                col_stats[idx] = "0.00"

        # Mark full columns explicitly
        for i in range(board.cols):
            if board.grid[0][i] != 0:
                col_stats[i] = "x"

        print("AI column win rates:", col_stats)

        best = min(root.children, key=lambda c: c.visits, default=None)
        return best.move if best else None


    def _select(self, node):
        if not node.children and not self._is_terminal(node.state):
            self._expand(node)
            if node.children:
                return node.children[0]
            else:
                return node  # Can't expand, treat as leaf
        if not node.children:
            return node  # Leaf node

        selected = max(node.children, key=lambda c: c.uct_score())
        return self._select(selected)


    def _expand(self, node):
        for col in range(1, node.state.cols + 1):
            if node.state.grid[0][col - 1] == 0:
                new_state = deepcopy(node.state)
                row = new_state.make_move(col, new_state.current_player)
                if row is None:
                    continue
                new_state.switch_player()
                child = MCTSNode(new_state, parent=node, move=col)
                node.children.append(child)

    def _simulate(self, state):
        sim = deepcopy(state)
        while True:
            winner = sim.check_winner()
            if winner or all(sim.grid[0][c] != 0 for c in range(sim.cols)):
                return winner
            moves = [c+1 for c in range(sim.cols) if sim.grid[0][c] == 0]
            col = self.heuristic_choose(moves, sim)
            sim.make_move(col, sim.current_player)
            sim.switch_player()

    def heuristic_choose(self, moves, state):
        # Prefer center columns
        center = state.cols // 2 + 1
        moves.sort(key=lambda c: -1/(abs(c - center) + epsilon))
        # Sometimes explore:
        return moves[0] if random.random() < 0.8 else random.choice(moves)

    def _backpropagate(self, node, winner):
        while node:
            node.visits += 1
            if winner == self.player:
                node.wins += 1
            node = node.parent


    def _is_terminal(self, state):
        return state.check_winner() or all(state.grid[0][c] != 0 for c in range(state.cols))
