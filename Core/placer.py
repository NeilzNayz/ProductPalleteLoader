import sys

class Item:
    pos_x: float = 0
    pos_y: float = 0

    def __init__(self, id:int, width:float, lenght:float, height:float) -> None:
        self.id = id
        self.width = width
        self.lenght = lenght
        self.height = height

def max_palette_load(p_lenght:float, p_width:float,
                     i_lenght:float, i_width:float) -> int:
    l1 = int(p_lenght / i_lenght) * int(p_width / i_width) + int((p_lenght % i_lenght) / i_width) * int(p_width/i_lenght)
    l2 = int(p_width / i_lenght) * int(p_lenght / i_width) + int((p_width % i_lenght) / i_width) * int(p_lenght/i_lenght)
    return max(l1,l2)

def calc(p_lenght:float, p_width:float, p_height:float,
         i_lenght:float, i_width:float, i_height:float,
         max_loaded_height:float) -> str:
    
    #Values check
    if p_height + i_height > max_loaded_height:
        raise ValueError(f"Value Error: Palette with items are higher then maximum allowed height\nmaximum allowed height: {max_loaded_height}\npalette and items heights: {p_height + i_height}")
    if max(p_lenght, p_width) > max(i_lenght, i_width) and min(p_lenght, p_width) > min(i_lenght, i_width) == False:
        raise ValueError(f"Value Error: Items are bigger than the palette.\nPalette size:{p_lenght}x{p_width}\nItem size:{i_lenght}x{i_width}")

    #Counting possible amount of items to load and making a list with them 
    max_load = max_palette_load(p_lenght, p_width, i_lenght, i_width)

    items:list[Item] = []
    for i in range(0, max_load):
        items.append(
            Item(id=i, lenght=i_lenght, width=i_width, height=i_height))

    return f"Max box on a palette is: {max_load}"