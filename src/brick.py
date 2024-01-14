from pygame import Surface

from src.utils import *


class Brick:
    
    def __init__(self, 
                 screen: Surface,
                 x: int, 
                 y: int, 
                 template: tuple[tuple[int, int]],
                 texture: Surface) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.texture = texture
        self.template = template
        self.template_to_coords()
    
    def template_to_coords(self) -> None:
        blocks = []
        for coord in self.template:
            blocks.append(
                (
                    X_CORNER + 32 * (self.x + coord[1]),
                    Y_CORNER + 32 * (self.y + coord[0] - 4)
                )
            )
        self.coords = tuple(blocks)
    
    def move(self, 
             x_add: int,
             y_add: int) -> None:
        self.x += x_add
        self.y += y_add
        self.template_to_coords()

    def draw(self) -> None:
        for coord in self.coords:
            self.screen.blit(self.texture, coord)
