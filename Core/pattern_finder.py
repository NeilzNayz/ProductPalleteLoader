from .models import Item, Rotation, Solution, Placing

def rotate_items(items:list[Item], start_index:int,end_index:int, rotation:Rotation):
    for item in items:
        l = item.lenght
        w = item.width
        if w > l and rotation == Rotation.Vertical or l > w and rotation == Rotation.Horizontal:
            item.rotate()

def generate_solution(p_lenght:float, p_width:float, total_items_amount:int, items:list[Item], rotation:Rotation)-> Solution:
    rotate_items(items, 0, items.__len__(), rotation)
    items_num = items.__len__()
    item_l = items[0].lenght
    item_w = items[0].width
    
    placing_mode = Placing.FromLeft   
    placed_i_row = 0
    placed_i_col = 0

    right_top_space:float = 0

    # Calculating and rotating items
    i_in_row = int(p_width / item_w)
    i_in_col = int(p_lenght / item_l)
    i_at_right:int = 0
    i_placed_at_right:int = 0
    i_at_top:int = 0
    i_placed_at_top:int = 0

    space_at_right = p_width - item_w * i_in_row
    if space_at_right < item_w and space_at_right >= item_l:
        rotate_items(items, i_in_row + i_in_col - 1, items_num, Rotation.Vertical)
        i_at_right = int(p_lenght / items[items_num].lenght)
        right_top_space = p_lenght - i_at_right * items[items_num].lenght
    
    space_at_top = p_lenght - item_l * i_in_col
    if space_at_top < item_l and space_at_top >= item_w:
        rotate_items(items, i_in_row + i_in_col + i_at_right - 1, items_num, Rotation.Horizontal)
        temp_p_width = p_width
        if(right_top_space < items[items_num].lenght):
            temp_p_width -= items[items_num].width
        i_at_top = int(temp_p_width / items[items_num].width)

    # Placing items
    for i in range(0, items_num):

        if placing_mode == Placing.FromLeft:
                items[i].pos_x = item_w * placed_i_row - item_w / 2
                items[i].pos_y = item_l * placed_i_col - item_l / 2
                placed_i_row += 1
                if(placed_i_row < i_in_row):
                    placed_i_row = 0
                    placed_i_col += 1
                if(placed_i_col < i_in_col):
                    placing_mode = Placing.AtRightSpace

        if placing_mode == Placing.AtRightSpace:
            if i_placed_at_right >= i_at_right:
                placing_mode = Placing.AtTopSpace
            items[i].pos_x = i_in_row * item_w + items[i].width / 2
            items[i].pos_y = i_placed_at_right * items[i].lenght + items[i].lenght / 2
            i_placed_at_right += 1

        if placing_mode == Placing.AtTopSpace:   
            if i_placed_at_top >= i_at_top:
                return Solution(items, i)         
            items[i].pos_x = i_placed_at_top * items[i].width + items[i].width / 2
            items[i].pos_y = i_in_col * item_l + items[i].lenght / 2
            i_placed_at_top += 1
                
    return Solution(items, items_num)    

def find_best_solution(p_lenght:float, p_width:float, total_items_amount:int, items:list[Item]) -> list[Solution]:

    #If sides are equal we just placing them
    if(items[0].width == items[0].lenght):
        return [generate_solution(p_lenght, p_width, total_items_amount, items.copy(), Rotation.NoRotation)]

    #Solutions
    v_solution:Solution = generate_solution(p_lenght, p_width, total_items_amount, items.copy(), Rotation.Vertical)
    h_solution:Solution = generate_solution(p_lenght, p_width, total_items_amount, items.copy(), Rotation.Horizontal)

    if h_solution.items_placed_num > v_solution.items_placed_num:
        return [h_solution]
    elif h_solution.items_placed_num < v_solution.items_placed_num:
        return [v_solution]
    else:
        return [h_solution, v_solution]
    
'''
Undone Formula for 'Basic' placing

y_mult = (i / i_in_row).__ceil__()
x_mult = (i - y_mult * 2).__ceil__()
if(x_mult > i_in_row):
    placing_mode = PlacingMode.SpaceAtRight
items[i].pos_x = item_w * x_mult - item_w / 2
items[i].pos_y = item_l * y_mult - item_l / 2
'''