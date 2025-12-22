from .pattern_finder import place_items
from .models import Item, Solution, Orientation, UserData
import math

def generate_solution(u_data:UserData, main_or:Orientation, orig_or:Orientation) -> Solution:
    """Generates a solution with a specific Main Orientation"""
    l1 = math.floor(u_data.p_l / u_data.i_l) * math.floor(u_data.p_w / u_data.i_w)
    l2 = math.floor(u_data.p_l / u_data.i_w) * math.floor(u_data.p_w / u_data.i_l)
    max_l = max(l1, l2)
 
    # "Aligning" item by MAIN orientation
    i_w = u_data.i_w if main_or == orig_or else u_data.i_l
    i_l = u_data.i_l if main_or == orig_or else u_data.i_w
    i_in_row = int(u_data.p_w / i_w)
    i_in_col = int(u_data.p_l / i_l)
    i_at_right = 0
    i_at_top = 0

    items:list[Item] = []
    for i in range(max_l):
        items.append(Item(i+1, u_data.i_l, u_data.i_w, u_data.i_h, main_or))

    if main_or is Orientation.Horizontal:
        if u_data.p_w - i_w * i_in_row >= i_l:
            i_at_right = int(u_data.p_l / i_w)
            for i in range(i_at_right):
                items.append(Item(max_l + i + 1, u_data.i_l, u_data.i_w, u_data.i_h, Orientation.Vertical))
    elif main_or is Orientation.Vertical:
        if u_data.p_l - i_l * i_in_col >= i_w:
            # "Aligning" item by HORIZONTAL orientation
            i_at_top = int(u_data.p_w / i_l)
            for i in range(i_at_top):
                items.append(Item(max_l + i + 1, u_data.i_l, u_data.i_w, u_data.i_h, Orientation.Horizontal))

    return place_items(u_data, items, i_in_row, i_in_col, i_at_right, i_at_top, max_l, orig_or)

# Generates array of solutions
def generate_solutions(u_data:UserData) -> list[Solution]:
    """Generates an array of solutions"""
    # --- Value check ---
    if min(u_data.p_l,u_data.p_w,u_data.p_h,u_data.i_l,u_data.i_w,u_data.i_h,u_data.max_h) <= 0:
        raise ValueError(f"Value Error: Values cannot be less than zero.\np_lenght:{u_data.p_l}\np_width:{u_data.p_w}\np_height:{u_data.p_h}\ni_lenght{u_data.i_l}\ni_width{u_data.i_w}\ni_height{u_data.i_h}")
    if u_data.p_h + u_data.i_h > u_data.max_h:
        raise ValueError(f"Value Error: Palette with items are higher then maximum allowed height\nmaximum allowed height: {u_data.max_h}\npalette and items heights: {u_data.p_h + u_data.i_h}")
    if max(u_data.p_l, u_data.p_w) > max(u_data.i_l, u_data.i_w) and min(u_data.p_l, u_data.p_w) > min(u_data.i_l, u_data.i_w) == False:
        raise ValueError(f"Value Error: Items are bigger than the palette.\nPalette size:{u_data.p_l}x{u_data.p_w}\nItem size:{u_data.i_l}x{u_data.i_w}")
    
    # --- Calculating best layout and generating solutions depending on it ---
    orig_or = Orientation.Vertical if u_data.i_l > u_data.i_w else Orientation.Horizontal
    solutions:list[Solution] = []
    solutions.append(generate_solution(u_data, Orientation.Vertical, orig_or))
    solutions.append(generate_solution(u_data, Orientation.Horizontal, orig_or))

    print(f'Which are pidorasi?')
    print(f'solution 1: {solutions[0].max_i}')
    print(f'solution 2: {solutions[1].max_i}')

    if solutions.__len__() > 1:
        if solutions[0].max_i == -1:
            solutions.remove(solutions[0])
        elif solutions[1].max_i == -1:
            solutions.remove(solutions[1])

    if solutions.__len__() > 1:
        if solutions[0].max_i > solutions[1].max_i:
            solutions.remove(solutions[1])
        elif solutions[0].max_i < solutions[1].max_i:
            solutions.remove(solutions[0])

    return solutions