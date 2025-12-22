from enum import Enum

class Orientation(Enum):
    Vertical=1,
    Horizontal=2,
    NoOrientation=3

class Item:
    def __init__(self, id:int, lenght:float, width:float, height:float, orientation) -> None:
        self.id = id
        self.width = width
        self.lenght = lenght
        self.height = height
        self.orientation = orientation
        self.pos_x = -20
        self.pos_y = -20

class Solution():
    def __init__(self, items:list[Item], main_or:Orientation, user_or:Orientation, i_main_or:int, i_additional:int, max_i:int) -> None:
        self.items = items
        self.main_or = main_or
        self.user_or = user_or
        self.i_main_or = i_main_or
        self.i_additional = i_additional
        self.max_i = max_i

class UserData():
    p_h = 0.0
    p_l = 0.0
    p_w = 0.0
    i_h = 0.0
    i_l = 0.0
    i_w = 0.0
    max_h = 0.0

class PlaceMode(Enum):
    FromLeft=1,
    AtRight=2,
    AtTop=3