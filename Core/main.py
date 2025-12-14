from .pattern_finder import generate_solution
from .models import Item, Solution, Orientation, UserData
import copy

def max_load_count(p_lenght:float, p_width:float, i_lenght:float, i_width:float) -> int:
    l1 = (p_lenght // i_lenght) * (p_width // i_width) + ((p_lenght % i_lenght) // i_width) * (p_width // i_lenght)
    l2 = (p_lenght // i_width) * (p_width // i_lenght) + ((p_lenght % i_width) // i_lenght) * (p_width // i_width)
    return int(max(l1,l2))

def generate_solutions(u_data:UserData) -> list[Solution]:
    #Value check
    if min(u_data.p_lenght,u_data.p_width,u_data.p_height,u_data.i_lenght,u_data.i_width,u_data.i_height,u_data.max_height) <= 0:
        raise ValueError(f"Value Error: Values cannot be less than zero.\np_lenght:{u_data.p_lenght}\np_width:{u_data.p_width}\np_height:{u_data.p_height}\ni_lenght{u_data.i_lenght}\ni_width{u_data.i_width}\ni_height{u_data.i_height}")
    if u_data.p_height + u_data.i_height > u_data.max_height:
        raise ValueError(f"Value Error: Palette with items are higher then maximum allowed height\nmaximum allowed height: {u_data.max_height}\npalette and items heights: {u_data.p_height + u_data.i_height}")
    if max(u_data.p_lenght, u_data.p_width) > max(u_data.i_lenght, u_data.i_width) and min(u_data.p_lenght, u_data.p_width) > min(u_data.i_lenght, u_data.i_width) == False:
        raise ValueError(f"Value Error: Items are bigger than the palette.\nPalette size:{u_data.p_lenght}x{u_data.p_width}\nItem size:{u_data.i_lenght}x{u_data.i_width}")

    #Calculating possible amount of items on a pallete
    max_load = max_load_count(u_data.p_lenght, u_data.p_width, u_data.i_lenght, u_data.i_width)
    print(f"MAXLOAD={max_load}")
    items:list[Item] = []
    for i in range(0, max_load):
        items.append(
            Item(id=i, lenght=u_data.i_lenght, width=u_data.i_width, height=u_data.i_height))

    #If sides are equal we just placing them
    if(items[0].width == items[0].lenght):
        return [generate_solution(u_data.p_lenght, u_data.p_width, items.copy(), Orientation.NoOrientation)]

    #Solutions
    v_solution:Solution = generate_solution(u_data.p_lenght, u_data.p_width, copy.deepcopy(items), Orientation.Vertical)
    h_solution:Solution = generate_solution(u_data.p_lenght, u_data.p_width, copy.deepcopy(items), Orientation.Horizontal)

    if h_solution.items_placed_num > v_solution.items_placed_num:   return [h_solution]
    elif h_solution.items_placed_num < v_solution.items_placed_num: return [v_solution]
    else: return [h_solution, v_solution]