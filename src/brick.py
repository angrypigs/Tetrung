from pygame import Surface

from src.utils import *


class Brick:
    
    def __init__(self, 
                 screen: Surface,
                 template: tuple[tuple[int, int]],
                 texture: Surface) -> None:
        self.screen = screen
        self.texture = texture
        self.template = template
    
    def place(self, 
              x: int | None = None, 
              y: int | None = None) -> None:
        blocks = []
        if x is not None and y is not None:
            self.x = x
            self.y = y
        x_min = min(self.template, key = lambda e: e[1])[1]
        y_min = min(self.template, key = lambda e: e[0])[0]
        for coord in self.template:
            blocks.append(
                (
                    self.x + 32 * (coord[1] - x_min),
                    self.y + 32 * (coord[0] - y_min)
                )
            )
        print(blocks)
        self.coords = tuple(blocks)

    def place_on_gridcell(self, 
                          x: int | None = None, 
                          y: int | None = None) -> None:
        blocks = []
        if x is not None and y is not None:
            self.x_grid = x
            self.y_grid = y
        for coord in self.template:
            blocks.append(
                (
                    X_CORNER + 32 * (self.x_grid + coord[1]),
                    Y_CORNER + 32 * (self.y_grid + coord[0])
                )
            )
        self.coords = tuple(blocks)
    
    def move(self, 
             x_add: int,
             y_add: int) -> None:
        self.x += x_add
        self.y += y_add
        self.place()

    def move_on_gridcell(self, 
                        x_add: int,
                        y_add: int) -> None:
        self.x_grid += x_add
        self.y_grid += y_add
        self.place_on_gridcell()
    
    def place_at_middle(self, x: int, y: int) -> None:
        x_min = min(self.template, key = lambda e: e[1])[1]
        x_max = max(self.template, key = lambda e: e[1])[1]
        y_min = min(self.template, key = lambda e: e[0])[0]
        y_max = max(self.template, key = lambda e: e[0])[0]
        self.place(x - (x_max - x_min + 1) * 16,
                   y - (y_max - y_min + 1) * 16)

    def draw(self) -> None:
        for coord in self.coords:
            self.screen.blit(self.texture, coord)
        
    


