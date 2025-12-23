# PalleteLoader v1.0

Loading maximum amount of items on a pallete

## Logs
`v1.0` Loads maximum of boxes on a pallete. That version has fully functional QT GUI. Full CLI version will be ready in on of the future versions. By default (without flags) runs QT GUI.

## How to use
1. Install all remaining packages from requirements.txt if you haven't  version with preinstalled packages.
2. Run `main.py` file in the root of the project with some flags if you need.

### Main.py flags
For now `main.py` has only 1 flag --gui=<gui_name>, and as I mentiond erlier CLI version isn't ready and it'll print that. But btw you still can check the code if you want.

#### Available flags:
1. `main.py --gui=qt` - Runs QT gui version
2. `main.py --gui=cli` - Runs CLI gui version

---

### QT usage
#### - Properties - section
To generate a solution on the left you'll see a pannel with properties. They are filled for an example, but can be cleared by `Clear All` button.

To generate solution you need to fill all properties and press `Generate Layouts` button.  After that it'll find best layouts (2 max) and visualize it on the right, black canvas

#### - SOLUTIONS - section
On the left panel `SOLUTIONS` lable'll appear. Under it there will be layouts switching buttons. Theyre amount depanding on an amount of found layouts. Pressing by them you'll see layouts that app found

#### - ITEM INFO - section
Lower you'll see `ITEM INFO` section. There you can get item's information by it's `id`. You'll find item's `id` on visualized layout on black canvas at right. 

---

### QT CLI usage
Works while app is working. Only can gice item information(position and rotation)

QT CLI has only 2 commands:
1. `lay <layout_num>` 
2. `item <item_num>`

Commands are available only if any solution was generated. To get Item information firstly select layout via `lay <layout_num>`. Example: `lay 1` - select layout 1. After that you can see item's information via `item <item_num>` Example: `item 7` print info about item with id 7.

#### Output

X: <pos_x>

Y: <pos_Y>

Z: <pos_Z>

A: <pos_A>