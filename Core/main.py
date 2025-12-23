from .pattern_finder import place_items
from .models import Item, Layout, Orientation, UserData
import math

def generate_solution(u_data:UserData, is_rotated:bool) -> Layout:
    """Generates a solution with a specific Main Orientation"""
    i_l = u_data.i_w if is_rotated else u_data.i_l
    i_w = u_data.i_l if is_rotated else u_data.i_w
    i_pos_z = u_data.p_h + u_data.i_h / 2
    i_in_row = math.floor(u_data.p_w / i_w)
    i_in_col = math.floor(u_data.p_l / i_l)
    max_l = i_in_row * i_in_col

    i_at_right = 0
    i_at_top = 0

    items:list[Item] = []
    for i in range(max_l):
        items.append(Item(i+1, i_l, i_w, i_pos_z, u_data.i_h, 90 if is_rotated else 0))

    if i_w > i_l:
        if u_data.p_w - i_w * i_in_row >= i_l:
            i_at_right = math.floor(u_data.p_l / i_w)
            for i in range(i_at_right):
                items.append(Item(max_l + i + 1, i_w, i_l, u_data.i_h, i_pos_z, 0 if is_rotated else 90))
    elif i_w < i_l:
        if u_data.p_l - i_l * i_in_col >= i_w:
            i_at_top = math.floor(u_data.p_w / i_l)
            for i in range(i_at_top):
                items.append(Item(max_l + i + 1, i_w, i_l, u_data.i_h, i_pos_z, 0 if is_rotated else 90))

    solution = place_items(u_data, items, i_in_row, i_in_col, i_at_right, i_at_top, max_l)
    for i in solution.items:
        i.lenght = u_data.i_l
        i.width = u_data.i_w
    return solution

# Generates array of solutions
def generate_layouts(u_data:UserData) -> list[Layout]:
    """Generates an array of solutions"""
    # --- Value check ---
    if min(u_data.p_l,u_data.p_w,u_data.p_h,u_data.i_l,u_data.i_w,u_data.i_h,u_data.max_h) <= 0:
        raise ValueError(f"Value Error: Values cannot be less than zero.\np_lenght:{u_data.p_l}\np_width:{u_data.p_w}\np_height:{u_data.p_h}\ni_lenght{u_data.i_l}\ni_width{u_data.i_w}\ni_height{u_data.i_h}")
    if u_data.p_h + u_data.i_h > u_data.max_h:
        raise ValueError(f"Value Error: Palette with items are higher then maximum allowed height\nmaximum allowed height: {u_data.max_h}\npalette and items heights: {u_data.p_h + u_data.i_h}")
    if max(u_data.p_l, u_data.p_w) > max(u_data.i_l, u_data.i_w) and min(u_data.p_l, u_data.p_w) > min(u_data.i_l, u_data.i_w) == False:
        raise ValueError(f"Value Error: Items are bigger than the palette.\nPalette size:{u_data.p_l}x{u_data.p_w}\nItem size:{u_data.i_l}x{u_data.i_w}")
    
    # --- Calculating best layout and generating solutions depending on it ---
    solutions:list[Layout] = []
    solutions.append(generate_solution(u_data, False))
    solutions.append(generate_solution(u_data, True))

    # --- Removing solutions with out of bounds boxes
    right_solutions:list[Layout] = []
    if solutions.__len__() > 1:
        for solution in solutions:
            if not solution.out_of_bounds:
                right_solutions.append(solution)

    # --- Removing solution with less items on a pallete
    if solutions.__len__() > 1:
        if solutions[0].max_i > solutions[1].max_i:
            solutions.remove(solutions[1])
        elif solutions[0].max_i < solutions[1].max_i:
            solutions.remove(solutions[0])

    return solutions