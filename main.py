import sys
import os

def help():
    print("Hren tebe")

if __name__ == "__main__":
    gui:str="none"
    item:str="none"
    inf_only:bool=False
    
    if sys.argv.__len__() == 0:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        target_file = os.path.join(project_dir, 'UI', 'qt', 'main.py')
        os.system(f'python3 {os.path.dirname(os.path.abspath(__file__))}')

    for arg in sys.argv:
        if arg == 'main.py':
            continue
        com:str
        val:str
        res = arg.find('=')

        #Checking for values
        if res != -1:
            args = arg.split('=')
            if args.__len__() < 2:
                print(f"Error: '{args[0]}' has empty value!")
                sys.exit()
            match args[0]:
                case "--gui":
                    project_dir = os.path.dirname(os.path.abspath(__file__))
                    target_file = os.path.join(project_dir, 'UI', args[1], 'main.py')
                    if os.path.exists(target_file):
                        os.system(f'python3 {target_file}')
                case _:
                    print(f"No argument named: {arg}")
        else:
            print(f"No argument named: {arg}")


            


