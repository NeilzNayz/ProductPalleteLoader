import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from Core.models import UserData
from models import Property, PropertiesList
import keyboard
import os

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

u_data:UserData = UserData()

pallete_properties:PropertiesList = PropertiesList("PALLETE PROPERTIES", [
    Property("Length"),
    Property("Width"),
    Property("Height")
])

pallete_properties:PropertiesList = PropertiesList("ITEM PROPERTIES", [
    Property("Length"),
    Property("Width"),
    Property("Height")
])

pallete_properties:PropertiesList = PropertiesList("ADDITIONAL PROPERTIES", [
    Property("Max height"),
])

all_options_lists = [
    pallete_properties,
    pallete_properties,
    pallete_properties
]

arrow_pos_y = 0
max_arrow_pos_y = 6

def drawFrame(options_lists:list[PropertiesList]):
    clear_screen()
    for list in options_lists:
        print(f'==================== {list.name} ====================')
        for i in range(0, list.props.__len__()):
            if i == arrow_pos_y:
                print(f'{list.props[i].name}: {list.props[i].input}  <--')
                
            else:
                print(f'{list.props[i].name}: {list.props[i].input}')

def moveArrow(add_by_y:int):
    global arrow_pos_y
    arrow_pos_y += add_by_y
    if arrow_pos_y > max_arrow_pos_y:
        arrow_pos_y = max_arrow_pos_y
    elif arrow_pos_y < 0:
        arrow_pos_y = 0

def hadleInput(key):
    match key:
        case 'up': moveArrow(-1)
        case 'down': moveArrow(1)
    drawFrame(all_options_lists)

def main():
    keyboard.hook(hadleInput)

if __name__ == "__main__":
    print("Not done yet...")
    

