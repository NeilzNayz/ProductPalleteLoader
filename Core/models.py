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
class UserData():
    p_height = 0.0
    p_lenght = 0.0
    p_width = 0.0
    i_height = 0.0
    i_lenght = 0.0
    i_width = 0.0
    max_height = 0.0

    is_p_height_correct = False
    is_p_lenght_correct = False
    is_p_width_correct = False
    is_i_height_correct = False
    is_i_lenght_correct = False
    is_i_width_correct = False
    is_max_height_correct = False

class PlaceMode(Enum):
    FromLeft=1,
    FillRightSpace=2,
    FillTopSpace=3
        