from enum import Enum

class Item:
    pos_x: float = -1
    pos_y: float = -1
    is_rotated = False
    def __init__(self, id:int, width:float, lenght:float, height:float) -> None:
        self.id = id
        self.width = width
        self.lenght = lenght
        self.height = height
    def rotate(self):
        temp = self.width
        self.width = self.lenght
        self.lenght = temp
        self.is_rotated = not self.is_rotated

class Solution():
    def __init__(self, items:list[Item], items_placed_num:int) -> None:
        self.items = items
        self.items_placed_num = items_placed_num

class Rotation(Enum):
    Vertical=1,
    Horizontal=2,
    NoRotation=3,

class Placing(Enum):
    FromLeft=1,
    AtRightSpace=2,
    AtTopSpace=3
        