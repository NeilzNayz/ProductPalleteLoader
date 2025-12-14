from Core.main import *
from Core.models import *
from Core.pattern_finder import *

def FirstAlgorithTest():
    solutions = generate_solutions(
        p_lenght=15.2,
        p_width =10.2,
        p_height=100,
        i_lenght=4.2,
        i_width =2.5,
        i_height=10,
        max_loaded_height=200
    )
    '''
    solutions = calc(
        p_lenght=12,
        p_width=8,
        p_height=100,
        i_lenght=2,
        i_width=3,
        i_height=10,
        max_loaded_height=2000
    )'''
    print(f"Num of solutions: {solutions.__len__()}")
    counter = 1
    for sol in solutions:
        print(f"== SOLUTION {counter} ==")
        print(f"Main orientation: {sol.main_orientation}")
        print(f"Placed items: {sol.items_placed_num}/{sol.possible_i_amount}")
        for j in range(0, sol.items.__len__()):
            item = sol.items[j]
            print(f"Item {j}\t{item.orientation}  pos_x{item.pos_x} pos_y{item.pos_y}  wid{item.width} len:{item.lenght}")
        counter+=1
if __name__ == "__main__":
    FirstAlgorithTest()


# Add 'out of bounds' check
# Add visualization on QT