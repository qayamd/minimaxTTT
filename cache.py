import pickle
from typing import Dict, Tuple, List, Optional
from node import TicTacToeNode
from search import heuristic, get_best_move

class TicTacToeCacheOptimizer:
    def __init__(self, cache_file: str = 'tictactoe_cache.pkl'):
        self.cache_file = cache_file
        self.cache: Dict[Tuple[str], Tuple[int, int]] = self.load_cache()

    def load_cache(self) -> Dict[Tuple[str], Tuple[int, int]]:
        try:
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_cache(self) -> None:
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def board_to_key(self, board: List[str]) -> Tuple[str]:
        return tuple(board)

    def cache_state(self, node: TicTacToeNode, value: int, best_move: int) -> None:
        key = self.board_to_key(node.board)
        self.cache[key] = (value, best_move)

    def get_cached_state(self, node: TicTacToeNode) -> Optional[Tuple[int, int]]:
        key = self.board_to_key(node.board)
        return self.cache.get(key)

    def generate_all_states(self, node: TicTacToeNode, depth: int = 9) -> None:
        if node.is_terminal() or depth == 0:
            value = heuristic(node)
            self.cache_state(node, value, -1)  # -1 indicates no move (terminal state)
            return

        best_value = float('-inf') if node.player == 'O' else float('inf')
        best_move = -1

        for i, child in enumerate(node.get_children()):
            self.generate_all_states(child, depth - 1)
            child_value, _ = self.get_cached_state(child)

            if node.player == 'O' and child_value > best_value:
                best_value = child_value
                best_move = i
            elif node.player == 'X' and child_value < best_value:
                best_value = child_value
                best_move = i

        self.cache_state(node, best_value, best_move)

    def optimize(self) -> None:
        initial_state = TicTacToeNode()
        self.generate_all_states(initial_state)
        self.save_cache()

# Modified get_best_move function to use the cache
def get_best_move_cached(node: TicTacToeNode, cache_optimizer: TicTacToeCacheOptimizer) -> TicTacToeNode:
    cached_value = cache_optimizer.get_cached_state(node)
    if cached_value:
        _, best_move_index = cached_value
        return node.get_children()[best_move_index]
    else:
        # Fallback to original minimax if state is not in cache (shouldn't happen if cache is complete)
        return get_best_move(node)

# Usage
cache_optimizer = TicTacToeCacheOptimizer()
cache_optimizer.optimize()  # Generate and cache all states (run this once)

# In the game loop, replace the call to get_best_move with:
# ai_move = get_best_move_cached(self.current_node, cache_optimizer)