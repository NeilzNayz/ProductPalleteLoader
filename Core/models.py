from enum import Enum

class Orientation(Enum):
    Vertical=1,
    Horizontal=2,
    NoOrientation=3

class Item:
    pos_x: float = -10
    pos_y: float = -10
    def __init__(self, id:int, width:float, lenght:float, height:float) -> None:
        self.id = id
        self.width = width
        self.lenght = lenght
        self.height = height
        self.orientation = Orientation.Horizontal if width > lenght  else Orientation.Vertical

class Solution():
    def __init__(self, items:list[Item], items_placed_num:int, main_orientation:Orientation, possible_i_amount:int) -> None:
        self.items = items
        self.items_placed_num = items_placed_num
        self.main_orientation = main_orientation
        self.possible_i_amount = possible_i_amount

class PlaceMode(Enum):
    FromLeft=1,
    FillRightSpace=2,
    FillTopSpace=3
        