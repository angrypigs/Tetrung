from src.utils import *
from random import randint, sample



class Board:

    def __init__(self) -> None:
        self.matrix = [[0 for x in range(10)] for y in range(25)]
        self.next_blocks = sample(range(1, 8), 3)
        self.current_block = randint(1, 7)
        self.current_state = 0
        self.row = 2
        self.col = 4
        self.rows_to_remove = []
        self.flag_placed = False

    def __place(self, 
                index: int,
                state: int,
                row: int,
                col: int) -> None:
        for coord in TEMPLATES[index - 1][state]:
            self.matrix[row + coord[0]][col + coord[1]] = index
        
    def __next_block(self) -> None:
        self.__place(self.current_block,
                     self.current_state,
                     self.row, self.col)
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(randint(1, 7))
        self.row, self.col = 2, 4
        self.current_state = 0
        for row in range(24, 0, -1):
            if self.matrix[row].count(0) == 0:
                self.rows_to_remove.append(row)
        self.rows_to_remove.sort()
        while self.rows_to_remove:
            s = self.rows_to_remove.pop(0)
            for row in range(s, 0, -1):
                if self.matrix[row].count(0) != 10:
                    self.matrix[row] = self.matrix[row - 1].copy()
                else:
                    break
        for i in self.matrix:
            print(i)

    def __is_fitting(self,
                    state: int,
                    row: int,
                    col: int) -> bool:
        for coord in TEMPLATES[self.current_block - 1][state]:
            a, b = row + coord[0], col + coord[1]
            if (b < 0 or b > 9 or a > 24 or
                self.matrix[a][b] != 0):
                return False
        return True
        
    def get_template(self) -> tuple[tuple[int, int]]:
        return TEMPLATES[self.current_block - 1][self.current_state]

    def move(self, row_add: int = 0, col_add: int = 0) -> bool:
        if self.__is_fitting(self.current_state,
                             self.row + row_add, self.col + col_add):
            self.row += row_add
            self.col += col_add
            return True
        return False

    def rotate(self) -> bool:
        if self.__is_fitting((self.current_state + 1) % 4,
                             self.row, self.col):
            self.current_state = (self.current_state + 1) % 4
            return True
        return False

    def instant_down(self) -> None:
        while True:
            if self.__is_fitting(self.current_state,
                                    self.row + 1, self.col):
                self.row += 1
            else:
                break
        self.__next_block()  

    def frame_move(self) -> str:
        if self.__is_fitting(self.current_state,
                             self.row + 1, self.col):
            self.row += 1
            return "moved"
        else:
            self.flag_placed = not self.flag_placed
            if not self.flag_placed:
                self.__next_block()
                return "changed"
        return "stayed"
