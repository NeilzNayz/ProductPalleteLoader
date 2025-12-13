from .models import Item, Orientation, Solution, PlaceMode

def rotate_items(items:list[Item], start_ind:int, end_ind:int, new_orientation:Orientation):
    if start_ind < 0: start_ind = 0
    if start_ind > items.__len__(): start_ind = items.__len__()
    if end_ind < 0: start_ind = 0
    if end_ind > items.__len__(): start_ind = items.__len__()
    for item in items[start_ind:end_ind]:
        l = item.lenght
        w = item.width
        if (new_orientation == Orientation.Vertical and w > l) or (new_orientation == Orientation.Horizontal and l > w):
            item.width = l
            item.lenght = w
        item.orientation = Orientation.Horizontal if item.width > item.lenght else Orientation.Vertical

def generate_solution(p_lenght:float, p_width:float, items:list[Item], i_orientation:Orientation)-> Solution:
    # Rotating as how rotation variable setted
    if i_orientation != Orientation.NoOrientation:
        rotate_items(items, 0, items.__len__(), i_orientation)
    items_num = items.__len__()
    item_l = items[0].lenght
    item_w = items[0].width
    i_in_row = int(p_width / item_w)
    i_in_col = int(p_lenght / item_l)
    placed_i_row = 0
    placed_i_col = 0
    place_mode = PlaceMode.FromLeft

    # Calculating potential free space (after placing items in setted orientation) and rotating items
    i_at_right:int = 0
    i_at_top:int = 0
    i_placed_at_right:int = 0
    i_placed_at_top:int = 0
    if i_orientation is Orientation.Horizontal:
        # If Space at right enoung for rotated item's width - rotate available items
        if p_width - item_w * i_in_row >= item_l:
            rotate_items(items, i_in_row * i_in_col, items_num, Orientation.Vertical)
            i_at_right = int(p_lenght / item_w) # item_w is rotated item's lenght
    elif i_orientation is Orientation.Vertical:
        # If Space at top enoung for rotated item's lenght - rotate available items
        if p_lenght - item_l * i_in_col >= item_w:
            rotate_items(items, i_in_row * i_in_col, items_num, Orientation.Horizontal)
            i_at_top = int(p_width / item_l) # item_l is rotated item's width

    # Placing items
    for i in range(0, items_num):
        if place_mode is PlaceMode.FromLeft:
            items[i].pos_x = item_w * (placed_i_row + 1)- item_w / 2
            items[i].pos_y = item_l * (placed_i_col + 1)- item_l / 2
            placed_i_row+=1
            if placed_i_row >= i_in_row:                    # If row filled - switch to another row, increace items in column counter
                placed_i_row = 0
                placed_i_col += 1
            if placed_i_col >= i_in_col:                    # If all colomns filled - change placing mode
                if(i_orientation == Orientation.Horizontal):
                    place_mode = PlaceMode.FillRightSpace
                elif(i_orientation == Orientation.Vertical):
                    place_mode = PlaceMode.FillTopSpace
                else:
                    return Solution(items, i + 1, i_orientation, items_num)
                continue

        if place_mode is PlaceMode.FillRightSpace:  
            if i_placed_at_right >= i_at_right:
                place_mode = PlaceMode.FillTopSpace
            items[i].pos_x = i_in_row * item_w + items[i].width / 2
            items[i].pos_y = i_placed_at_right * items[i].lenght + items[i].lenght / 2
            i_placed_at_right += 1

        if place_mode is PlaceMode.FillTopSpace:   
            if i_placed_at_top >= i_at_top:
                return Solution(items, i + 1, i_orientation, items_num)         
            items[i].pos_x = i_placed_at_top * items[i].width + items[i].width / 2
            items[i].pos_y = i_in_col * item_l + items[i].lenght / 2
            i_placed_at_top += 1
                
    return Solution(items, items_num, i_orientation, items_num)

'''
Undone formula for 'Basic' placing

y_mult = (i / i_in_row).__ceil__()
x_mult = (i - y_mult * 2).__ceil__()
if(x_mult > i_in_row):
    placing_mode = PlacingMode.SpaceAtRight
items[i].pos_x = item_w * x_mult - item_w / 2
items[i].pos_y = item_l * y_mult - item_l / 2
'''