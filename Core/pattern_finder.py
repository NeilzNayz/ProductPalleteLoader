from .models import Item, Orientation, Layout, PlaceMode, UserData

def outside_pallete(u_data:UserData, item:Item) -> bool:
    """Checks is item touching the outisde of a pallete"""
    top    = item.pos_y + item.lenght / 2
    right  = item.pos_x + item.width  / 2
    left   = item.pos_x - item.width  / 2
    bottom = item.pos_y - item.lenght / 2
    if (top > u_data.p_l or right > u_data.p_w) or (left < 0 or bottom < 0):
        return True
    return False

def place_items(u_data:UserData, items:list[Item], i_in_row:int, i_in_col:int, i_at_right:int, i_at_top:int, max_l:int)-> Layout:
    i_num = items.__len__()
    placed_i_row = 0
    placed_i_col = 0
    i_w = items[0].width
    i_l = items[0].lenght

    # --- Placing items by main layout ---
    for i in range(0, max_l):
        items[i].pos_x = i_w * (placed_i_row + 1) - i_w / 2
        items[i].pos_y = i_l * (placed_i_col + 1) - i_l / 2
        if outside_pallete(u_data, items[i]):
            return Layout(items, 0.0, max_l, i_at_right + i_at_top, i_num, True)
        placed_i_row += 1
        if placed_i_row >= i_in_row:
            placed_i_row = 0
            placed_i_col += 1
        
    # --- Placing items at RIGHT if free space was found there ---
    if i_at_right > 0:
        for i in range(max_l, i_num):
            items[i].pos_x = i_in_row * i_w + items[i].width / 2
            items[i].pos_y = (i - max_l) * items[i].lenght + items[i].lenght / 2
            if outside_pallete(u_data, items[i]):
                return Layout(items, 0.0, max_l, i_at_right + i_at_top, i_num, True)
    # --- Placing items at TOP if free space was found there ---
    elif i_at_top > 0:
        for i in range(max_l, i_num):
            items[i].pos_x = (i - max_l) * items[i].width + items[i].width / 2
            items[i].pos_y = i_in_col * i_l + i_w / 2
            if outside_pallete(u_data, items[i]):
                return Layout(items, 0.0, max_l, i_at_right + i_at_top, i_num, True)
                
    return Layout(items, items[0].rot_z, max_l, i_at_right + i_at_top, i_num, False)