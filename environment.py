import pygame
import sys
from node import TicTacToeNode
from typing import List, Optional, Tuple
from search import minimax, get_best_move
from cache import TicTacToeCacheOptimizer, get_best_move_cached

class TicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.font: pygame.font.Font = pygame.font.Font(None, 74)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.cache_optimizer = TicTacToeCacheOptimizer()
        self.cache_optimizer.optimize()
        self.reset_game()

    def reset_game(self) -> None:
        self.current_node: TicTacToeNode = TicTacToeNode()
        self.game_over: bool = False
        self.winner: Optional[str] = None

    def draw_board(self) -> None:
        self.screen.fill((255, 255, 255))
        pygame.draw.line(self.screen, (0, 0, 0), (100, 0), (100, 300), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (200, 0), (200, 300), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 100), (300, 100), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 200), (300, 200), 2)

        for i, mark in enumerate(self.current_node.board):
            if mark != ' ':
                x = i % 3 * 100 + 50
                y = i // 3 * 100 + 50
                text = self.font.render(mark, True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rect)

    def handle_click(self, pos: Tuple[int, int]) -> None:
        if self.game_over or self.current_node.player != 'X':
            return

        x, y = pos
        row = y // 100
        col = x // 100
        index = row * 3 + col

        new_node = self.current_node.make_move(index)
        if new_node:
            self.current_node = new_node
            self.check_game_over()
            
        if not self.game_over:
            self.current_node = get_best_move_cached(self.current_node, self.cache_optimizer)
            self.check_game_over()

    def check_game_over(self) -> None:
        if self.current_node.is_terminal():
            self.game_over = True
            if self.current_node.is_winner('X'):
                self.winner = 'X'
            elif self.current_node.is_winner('O'):
                self.winner = 'O'

    def display_winner(self) -> None:
        if self.winner:
            text = f"{self.winner} wins!"
        else:
            text = "It's a draw!"
        text_surface = self.font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(150, 150))
        self.screen.blit(text_surface, text_rect)

        restart_text = self.small_font.render("Click to play again", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(150, 250))
        self.screen.blit(restart_text, restart_rect)

    def play(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.handle_click(pygame.mouse.get_pos())

            self.draw_board()
            if self.game_over:
                self.display_winner()

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = TicTacToeGame()
    game.play()