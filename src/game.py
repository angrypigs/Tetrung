import pygame
import sys



class Game:

    def __init__(self) -> None:
        self.WIDTH = 600
        self.HEIGHT = 880
        self.FPS = 60
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tetrung")
        self.run = True
        self.clock = pygame.time.Clock()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()