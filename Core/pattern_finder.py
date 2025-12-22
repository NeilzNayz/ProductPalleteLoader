from .models import Item, Orientation, Solution, PlaceMode, UserData

def is_inside_pallete(u_data:UserData, item:Item, i_w:float, i_l:float) -> bool:
    i_top = item.pos_y + i_l / 2
    i_right = item.pos_x + i_w / 2
    if i_top > u_data.p_l or i_right > u_data.p_w:
        return False
    return True

def place_items(u_data:UserData, items:list[Item], i_in_row:int, i_in_col:int, i_at_right:int, i_at_top:int, max_l:int, user_or:Orientation)-> Solution:
    """Places items on a pallete."""
    i_num = items.__len__()
    placed_i_row = 0
    placed_i_col = 0
    i_w = u_data.i_w if items[0].orientation == user_or else u_data.i_l
    i_l = u_data.i_l if items[0].orientation == user_or else u_data.i_w

    # --- Placing items by main layout ---
    for i in range(0, max_l):
        items[i].pos_x = i_w * (placed_i_row + 1) - i_w / 2
        items[i].pos_y = i_l * (placed_i_col + 1) - i_l / 2
        if not is_inside_pallete(u_data, items[i], i_w, i_l):
            return Solution(items, Orientation.NoOrientation, user_or, -1, -1, -1)
        placed_i_row += 1
        if placed_i_row >= i_in_row:
            placed_i_row = 0
            placed_i_col += 1
        
    # --- Placing items at free space at RIGHT if main layout is HORIZONTAL ---
    if i_at_right > 0:
        for i in range(max_l, i_num):
            items[i].pos_x = i_in_row * i_w + i_l / 2
            items[i].pos_y = (i - max_l) * i_w + i_w / 2
            if not is_inside_pallete(u_data, items[i], i_w, i_l):
                return Solution(items, Orientation.NoOrientation, user_or, -1, -1, -1)
    # --- Placing items at free space at TOP if main layout is VERTICAL ---
    elif i_at_top > 0:
        for i in range(max_l, i_num):
            items[i].pos_x = (i - max_l) * i_l + i_w / 2
            items[i].pos_y = i_in_col * i_l + i_w / 2
            if not is_inside_pallete(u_data, items[i], i_w, i_l):
                return Solution(items, Orientation.NoOrientation, user_or, -1, -1, -1)
                
    return Solution(items, items[0].orientation, user_or, max_l, i_at_right + i_at_top, i_num)