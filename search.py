from node import TicTacToeNode
from typing import Tuple

def heuristic(node: TicTacToeNode) -> int:
    score = 0
    board = node.board
    if node.is_winner("O"):
        score = 1000
        return score
    elif node.is_winner("X"):
        score = -1000
        return score
    elif node.is_terminal():
        return 0
    
    # Enumerate all rows, columns and diagonals
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for line in lines:
        ai_count = sum(1 for i in line if board[i] == "O")
        human_count = sum(1 for i in line if board[i] == "X")
        
        if human_count == 0:
            score += 10 * ai_count
        elif ai_count == 0:
            score -= 10 * human_count
    
    # Control of strategic positions
    center_index = 4
    corner_indices = [0, 2, 6, 8]
    
    if board[center_index] == "O":
        score += 3
    elif board[center_index] == "X":
        score -= 3
    
    for corner in corner_indices:
        if board[corner] == "O":
            score += 2
        elif board[corner] == "X":
            score -= 2   
    
    return score

def minimax(node: TicTacToeNode, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[int, TicTacToeNode]:
    if depth == 0 or node.is_terminal():
        return heuristic(node), node

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for child in node.get_children():
            eval, _ = minimax(child, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for child in node.get_children():
            eval, _ = minimax(child, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move(node: TicTacToeNode, depth: int = 9) -> TicTacToeNode:
    _, best_move = minimax(node, depth, float('-inf'), float('inf'), True)
    return best_move