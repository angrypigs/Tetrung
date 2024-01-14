import pygame
import sys

from src.utils import *
from src.board import Board
from src.brick import Brick



class Game:

    def __init__(self) -> None:
        self.FPS = 60
        self.__init_images()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetrung")
        self.clock = pygame.time.Clock()
        self.run = True
        self.counter = 0
        self.board = Board()
        self.current_block = Brick(self.screen, 4, 2,
                                   self.board.get_template(),
                                   self.IMAGES["blocks"][self.board.current_block - 1])
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.board.move(col_add = 1):
                            self.current_block.move(1, 0)
                    elif event.key == pygame.K_LEFT:
                        if self.board.move(col_add = -1):
                            self.current_block.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        if self.board.move(row_add = 1):
                            self.current_block.move(0, 1)
                    elif event.key == pygame.K_UP:
                        if self.board.rotate():
                            self.current_block.template = self.board.get_template()
                            self.current_block.template_to_coords()
                    elif event.key == pygame.K_SPACE:
                        self.board.instant_down()
                        self.current_block = Brick(self.screen,
                                                   4, 2, self.board.get_template(),
                                                   self.IMAGES["blocks"][self.board.current_block - 1])
            self.counter = (self.counter + 1) % 900
            if self.counter % 30 == 0:
                match self.board.frame_move():
                    case "moved":
                        self.current_block.move(0, 1)
                    case "changed":
                        self.current_block = Brick(self.screen,
                                                   4, 2, self.board.get_template(),
                                                   self.IMAGES["blocks"][self.board.current_block - 1])
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            
        pygame.quit()
        sys.exit()

    def draw_game(self) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.IMAGES["gridcell"], (X_CORNER, Y_CORNER))
        for row in range(25):
            for col in range(10):
                if self.board.matrix[row][col] != 0:
                    self.screen.blit(self.IMAGES["blocks"][self.board.matrix[row][col] - 1],
                                     (X_CORNER + 32 * col, Y_CORNER + 32 * (row - 5)))
        self.current_block.draw()

    def __init_images(self) -> None:
        self.IMAGES = {
            "blocks": [
                pygame.image.load(res_path("assets/bricks/I_block.png")),
                pygame.image.load(res_path("assets/bricks/J_block.png")),
                pygame.image.load(res_path("assets/bricks/L_block.png")),
                pygame.image.load(res_path("assets/bricks/O_block.png")),
                pygame.image.load(res_path("assets/bricks/S_block.png")),
                pygame.image.load(res_path("assets/bricks/T_block.png")),
                pygame.image.load(res_path("assets/bricks/Z_block.png"))
            ],
            "buttons": {
                "exit": pygame.image.load(res_path("assets/buttons/button_exit.png")),
                "go": pygame.image.load(res_path("assets/buttons/button_go.png")),
                "house": pygame.image.load(res_path("assets/buttons/button_house.png")),
                "keyboard": pygame.image.load(res_path("assets/buttons/button_keyboard.png")),
                "pause": pygame.image.load(res_path("assets/buttons/button_pause.png")),
                "play": pygame.image.load(res_path("assets/buttons/button_play.png")),
            },
            "gridcell": pygame.image.load(res_path("assets/game_bg.png")),
            "logo": pygame.image.load(res_path("assets/tetrung_logo.png"))
        }