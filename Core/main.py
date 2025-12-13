from .pattern_finder import generate_solution
from .models import Item, Solution, Orientation
import copy

def max_load_count(p_lenght:float, p_width:float,
                     i_lenght:float, i_width:float) -> int:
    l1 = (p_lenght // i_lenght) * (p_width // i_width) + ((p_lenght % i_lenght) // i_width) * (p_width // i_lenght)
    l2 = (p_lenght // i_width) * (p_width // i_lenght) + ((p_lenght % i_width) // i_lenght) * (p_width // i_width)
    
    return int(max(l1,l2))

def calc(p_lenght:float, p_width:float, p_height:float,
         i_lenght:float, i_width:float, i_height:float,
         max_loaded_height:float) -> list[Solution]:
    #Value check
    if min(p_lenght,p_width,p_height,i_lenght,i_width,i_height,max_loaded_height) < 0:
        raise ValueError(f"Value Error: Values cannot be less than zero.\np_lenght:{p_lenght}\np_width:{p_width}\np_height:{p_height}\ni_lenght{i_lenght}\ni_width{i_width}\ni_height{i_height}")
    if p_height + i_height > max_loaded_height:
        raise ValueError(f"Value Error: Palette with items are higher then maximum allowed height\nmaximum allowed height: {max_loaded_height}\npalette and items heights: {p_height + i_height}")
    if max(p_lenght, p_width) > max(i_lenght, i_width) and min(p_lenght, p_width) > min(i_lenght, i_width) == False:
        raise ValueError(f"Value Error: Items are bigger than the palette.\nPalette size:{p_lenght}x{p_width}\nItem size:{i_lenght}x{i_width}")

    #Calculating possible amount of items on a pallete
    max_load = max_load_count(p_lenght, p_width, i_lenght, i_width)
    print(f"MAXLOAD={max_load}")
    items:list[Item] = []
    for i in range(0, max_load):
        items.append(
            Item(id=i, lenght=i_lenght, width=i_width, height=i_height))

    #If sides are equal we just placing them
    if(items[0].width == items[0].lenght):
        return [generate_solution(p_lenght, p_width, items.copy(), Orientation.NoOrientation)]

    #Solutions
    v_solution:Solution = generate_solution(p_lenght, p_width, copy.deepcopy(items), Orientation.Vertical)
    h_solution:Solution = generate_solution(p_lenght, p_width, copy.deepcopy(items), Orientation.Horizontal)

    if h_solution.items_placed_num > v_solution.items_placed_num:   return [h_solution]
    elif h_solution.items_placed_num < v_solution.items_placed_num: return [v_solution]
    else: return [h_solution, v_solution]