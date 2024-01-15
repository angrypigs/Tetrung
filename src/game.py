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
        self.pause = False
        self.counter = 0
        self.board = Board()
        self.current_block = Brick(self.screen, 4, 4,
                                   self.board.get_template(),
                                   self.IMAGES["blocks"][self.board.current_block - 1])
        self.next_blocks : list[Brick] = []
        for i in range(3):
            self.next_blocks.append(Brick(self.screen,
                                          13, 7 + i * 5,
                                          TEMPLATES[self.board.next_blocks[i] - 1][0],
                                          self.IMAGES["blocks"][self.board.next_blocks[i] - 1]))
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if not self.pause and self.board.move(col_add = 1):
                            self.current_block.move(1, 0)
                    elif event.key == pygame.K_LEFT:
                        if not self.pause and self.board.move(col_add = -1):
                            self.current_block.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        if not self.pause and self.board.move(row_add = 1):
                            self.current_block.move(0, 1)
                    elif event.key == pygame.K_UP:
                        if not self.pause and self.board.rotate():
                            self.current_block.template = self.board.get_template()
                            self.current_block.template_to_coords()
                    elif event.key == pygame.K_SPACE:
                        if not self.pause:
                            self.board.instant_down()
                            self.change_next_bricks()
                    elif event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause
            self.counter = (self.counter + 1) % 900
            if not self.pause and self.counter % 30 == 0:
                match self.board.frame_move():
                    case "moved":
                        self.current_block.move(0, 1)
                    case "changed":
                        self.change_next_bricks()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            
        pygame.quit()
        sys.exit()

    def change_next_bricks(self) -> None:
        self.current_block = Brick(self.screen,
                                    4, 4, self.board.get_template(),
                                    self.IMAGES["blocks"][self.board.current_block - 1])
        self.next_blocks.pop(0)
        self.next_blocks[0].move(0, -5)
        self.next_blocks[1].move(0, -5)
        self.next_blocks.append(Brick(self.screen,
                            13, 17,
                            TEMPLATES[self.board.next_blocks[2] - 1][0],
                            self.IMAGES["blocks"][self.board.next_blocks[2] - 1]))

    def draw_game(self) -> None:
        self.screen.fill((15, 65, 120))
        self.screen.blit(self.IMAGES["gridcell"], (X_CORNER, Y_CORNER))
        pygame.draw.rect(self.screen, (11, 47, 85), 
                         (X_CORNER + 352, Y_CORNER, 160, 640))
        for next_block in self.next_blocks:
            next_block.draw()
        for row in range(25):
            for col in range(10):
                if self.board.matrix[row][col] != 0:
                    self.screen.blit(self.IMAGES["blocks"][self.board.matrix[row][col] - 1],
                                     (X_CORNER + 32 * col, Y_CORNER + 32 * (row - 5)))
        self.current_block.draw()
        pygame.draw.rect(self.screen, (15, 65, 120),
                         (X_CORNER, 0, 320, Y_CORNER))

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