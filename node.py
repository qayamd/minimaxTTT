from typing import List, Optional, Tuple

class TicTacToeNode:
    def __init__(self, board: Optional[List[str]] = None, player: str = 'X'):
        self.board: List[str] = board if board else [' '] * 9
        self.player: str = player

    def get_empty_cells(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def make_move(self, position: int) -> Optional['TicTacToeNode']:
        if self.board[position] == ' ':
            new_board = self.board.copy()
            new_board[position] = self.player
            return TicTacToeNode(new_board, 'O' if self.player == 'X' else 'X')
        return None

    def is_winner(self, player: str) -> bool:
        winning_combinations: List[List[int]] = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(self.board[i] == player for i in combo) for combo in winning_combinations)

    def is_terminal(self) -> bool:
        return self.is_winner('X') or self.is_winner('O') or ' ' not in self.board

    def get_children(self) -> List['TicTacToeNode']:
        return [self.make_move(pos) for pos in self.get_empty_cells() if self.make_move(pos) is not None]

    def evaluate(self) -> int:
        if self.is_winner('X'):
            return 1
        elif self.is_winner('O'):
            return -1
        else:
            return 0