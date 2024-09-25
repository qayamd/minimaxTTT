# Tic Tac Toe AI

## What is it?
This repo contains an implementation of a Tic Tac Toe AI agent using the Minimax algorithm with alpha-beta pruning and a custom heuristic function. The AI is designed to play optimally against human players, making it unbeatable in most scenarios.

## How does the AI work?
The AI uses the Minimax algorithm, a decision-making algorithm for turn-based games. It explores all possible future game states to determine the best move. Alpha-beta pruning is employed to optimize the search process by eliminating branches that don't need to be explored.

The algorithm can be visualized as a tree of possible moves:

```
       Root
    /   |   \
   /    |    \
Node1 Node2 Node3
 / \    |    / \
...    ...    ...
```

Each node represents a game state, and the AI evaluates these states using a heuristic function to determine the best path.

## Why is it efficient?
The AI's efficiency comes from two main components: the Minimax algorithm with alpha-beta pruning and the custom heuristic function.

### Minimax with Alpha-Beta Pruning
Minimax allows the AI to consider all possible future game states, while alpha-beta pruning significantly reduces the number of nodes that need to be evaluated. 
This pruning technique can drastically reduce the search space, especially in complex game trees, making the AI more efficient.

### Heuristic Function
The heuristic function in `search.py` evaluates non-terminal game states, providing a score that represents the favorability of the position for the AI. Key aspects of the heuristic include:

1. Immediate win/loss detection
2. Evaluation of potential winning lines
3. Control of strategic positions (center and corners)

This heuristic allows the AI to make informed decisions even when it can't search to the end of the game, balancing performance and decision quality.

## When is it more efficient?
The efficiency of this AI becomes more apparent in the following scenarios:

1. Mid-game situations with multiple possible moves
2. When playing against skilled opponents who force the AI to consider complex sequences
3. In time-constrained environments where quick decision-making is crucial

## What does what?
* `environment.py`: Implements the game environment using Pygame, handling the game loop and user interactions.
* `node.py`: Defines the `TicTacToeNode` class, representing game states and providing methods for game logic.
* `search.py`: Contains the Minimax algorithm implementation with alpha-beta pruning and the heuristic function.

