import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from Core.models import UserData, Layout, Item
from Core.main import generate_layouts
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtGui import QGuiApplication, QBrush, QPen, QColor
from PyQt6 import QtWidgets
from UI.qt.models import ProductItem, ZoomableGraphicsView, CenteredLabel, InvisableLable

def clear_console():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

class InputThread(QThread):
    input_recieved = pyqtSignal(str)
    print("command:", end=' ')
    def run(self):
        while True:
            user_input = input()
            self.input_recieved.emit(user_input)

class MainWindow(QMainWindow):

    # Increases items size when Visualizing
    SIZE_MULTIPLAYER = 30

    # ================ Buttons and Fields logics ================
    def set_text_visable(self, input_field:QLabel, text:str):
        input_field.setText(text)
        input_field.setVisible(True)

    def btn_generate_exmaple_logic(self):
        self.field_inputs[0].setText(str(15.2))
        self.field_inputs[1].setText(str(10.2))
        self.field_inputs[2].setText(str(1))
        self.field_inputs[3].setText(str(4))
        self.field_inputs[4].setText(str(2.5))
        self.field_inputs[5].setText(str(1))
        self.field_inputs[6].setText(str(12))
        self.btn_generate_logic()

    def btn_clear_all_logic(self):
        for field in self.field_inputs:
            field.setText('')

    def btn_switch_layout(self, layout_ind):
        self.selected_layout_ind = layout_ind
        self.visualize_layout(self.items_layouts[layout_ind])
        self.lable_i_num_lable.setText(f'Items in layer: {self.items_layouts[layout_ind].max_i}')
        self.lable_layers_num.setText(f'Layers can be placed: {(self.u_data.max_h - self.u_data.p_h) / self.u_data.i_h}')
        self.check_item_id()

        if self.btn_find_item.isEnabled():
            self.show_item_info()
        self.btns_layouts[layout_ind].setDisabled(True)
        for i in range(0, self.btns_layouts.__len__()):
            if(i != layout_ind):
                self.btns_layouts[i].setDisabled(False)

    def check_item_id(self):
        i_ind = self.input_field_item_id.text()
        if i_ind.isspace() or i_ind == '':
            self.input_field_item_id.setStyleSheet('color: white;')
            return
        try:
            i_ind = int(i_ind)
            if i_ind <= self.items_layouts[0].max_i and i_ind > 0:
                self.input_field_item_id.setStyleSheet('color: rgb(3, 252, 7);')
                self.btn_find_item.setEnabled(True)
                return
        except:
            self.input_field_item_id.setStyleSheet('color: red;')
        self.input_field_item_id.setStyleSheet("color: red;")
        self.btn_find_item.setEnabled(False)

    def show_item_info(self):
        i_ind = int(self.input_field_item_id.text()) - 1
        self.input_field_item_id.setStyleSheet("color: rgb(3, 252, 7);")
        item:Item = self.items_layouts[self.selected_layout_ind].items[i_ind]
        self.set_text_visable(self.label_item_pos_x, f'X: {item.pos_x}')
        self.set_text_visable(self.label_item_pos_y, f'Y: {item.pos_y}')
        self.set_text_visable(self.label_item_pos_z, f'Z: {item.pos_z}')
        self.set_text_visable(self.label_item_rotation_a, f'A: {item.rot_z}')

    def btn_generate_logic(self):
        # Value Check
        if  self.u_data.p_l == 0 or \
            self.u_data.p_w == 0 or \
            self.u_data.p_h == 0 or \
            self.u_data.i_l == 0 or \
            self.u_data.i_w == 0 or \
            self.u_data.i_h == 0 or \
            self.u_data.max_h == 0:
                return
        
        # Making item's info lables invisiable
        self.label_item_pos_x.setVisible(False)
        self.label_item_pos_y.setVisible(False)
        self.label_item_pos_z.setVisible(False)
        self.label_item_rotation_a.setVisible(False)
        self.input_field_item_id.setText('')

        # generating layouts
        self.items_layouts = generate_layouts(self.u_data)

        # Checking if any layout was made 
        sol_num = self.items_layouts.__len__()
        if sol_num > 0:
            if sol_num == 1:
                self.btns_layouts[0].setVisible(True)
                self.btns_layouts[0].setEnabled(False)
            else:
                for btn in self.btns_layouts:
                    btn.setVisible(True)
                    btn.setEnabled(True)
            self.btns_layouts[0].setChecked(True)
            self.btn_switch_layout(0)

    # ================ Widgets creating Templates ================
    def create_btn_switch_layout(self, layout_num:int) -> QPushButton:
        btn = QPushButton(str(layout_num))
        btn.setEnabled(False)
        btn.setVisible(False)
        btn.setCheckable(True)
        btn.pressed.connect(lambda: self.btn_switch_layout(layout_num - 1))
        return btn
    
    def check_field_value(self, text:str, field_var_name:str, field_lable:QLabel):
        if text.isspace() or text == '':
            setattr(self.u_data, f'{field_var_name}', 0)
            field_lable.setStyleSheet("color: white")
            self.generate_button.setEnabled(False)
            return
        try:
            setattr(self.u_data, field_var_name, float(text))
            field_lable.setStyleSheet("color: rgb(3, 252, 7)")
            self.generate_button.setEnabled(True)
        except:
            setattr(self.u_data, f'{field_var_name}', 0)
            field_lable.setStyleSheet("color: red")
            self.generate_button.setEnabled(False)

    def create_field_layout(self, name, field_var_name):
        """Creates layout that contains variable's field and lable"""
        field_layout = QHBoxLayout()
        field_lable = QLabel(f"{name}: ")
        field_line_edit = QLineEdit()
        field_line_edit.setObjectName(f'input_field_{name}')
        field_line_edit.textChanged.connect(lambda text: self.check_field_value(text, field_var_name, field_lable))
        self.field_inputs.append(field_line_edit)
        field_layout.addWidget(field_lable)
        field_layout.addWidget(field_line_edit)
        return field_layout
    
    # ================ Draws pallete and items ================
    def visualize_layout(self, layout:Layout):
        # Visualizing pallete
        self.graphic_scene.clear()
        pallet = QGraphicsRectItem(0, 0, self.u_data.p_w * self.SIZE_MULTIPLAYER, self.u_data.p_l * self.SIZE_MULTIPLAYER)
        pallet.setBrush(QBrush(Qt.GlobalColor.transparent))
        pallet.setPen(QPen(QColor('brown')))
        self.graphic_scene.addItem(pallet)

        # Visualizing items
        for item in layout.items:
            rect_i = ProductItem(item, self.u_data, self.SIZE_MULTIPLAYER)
            self.graphic_scene.addItem(rect_i)

    # ================ UI Initialization ================
    def init_ui(self):
        """Initializes left ui panel, canvas, etc"""
        # --- Creating conrainers ---
        main_container = QWidget()
        layout_main = QHBoxLayout()
        main_container.setLayout(layout_main)
        self.field_inputs:list[QLineEdit] = []
        self.ui_panel_container = QWidget()
        self.ui_panel_container.setFixedWidth(250)
        layout_ui_panel = QVBoxLayout()
        self.ui_panel_container.setLayout(layout_ui_panel)
        self.ui_panel_container.setStyleSheet('background-color: rgb(40, 40, 40)')

        # --- User fields and buttons ---
        layout_ui_panel.addWidget(CenteredLabel('PALLETE PROPERTIES'))
        layout_ui_panel.addLayout(self.create_field_layout('Lenght', 'p_l'))
        layout_ui_panel.addLayout(self.create_field_layout('Width',  'p_w' ))
        layout_ui_panel.addLayout(self.create_field_layout('Height', 'p_h'))
        layout_ui_panel.addSpacing(15)
        layout_ui_panel.addWidget(CenteredLabel("ITEM PROPERTIES"))
        layout_ui_panel.addLayout(self.create_field_layout('Lenght', 'i_l'))
        layout_ui_panel.addLayout(self.create_field_layout('Width',  'i_w' ))
        layout_ui_panel.addLayout(self.create_field_layout('Height', 'i_h'))
        layout_ui_panel.addSpacing(15)
        layout_ui_panel.addWidget(CenteredLabel('ADDITIONAL PROPERTIES'))
        layout_ui_panel.addLayout(self.create_field_layout('Max height', 'max_h'))
        layout_ui_panel.addSpacing(15)

        self.generate_button = QPushButton('Generate Layouts')
        self.generate_button.setStyleSheet('color: white')
        self.generate_button.pressed.connect(self.btn_generate_logic)

        btn_generate_exmaple = QPushButton('Generate Example')
        btn_generate_exmaple.setStyleSheet('background-color: rgb(80,0,80); color: white')
        btn_generate_exmaple.clicked.connect(self.btn_generate_exmaple_logic)

        btn_clear_all = QPushButton('Clear All')
        btn_clear_all.setStyleSheet('background-color: rgb(130,0,0); color: white')
        btn_clear_all.clicked.connect(self.btn_clear_all_logic)
        
        layout_ui_panel.addWidget(self.generate_button)
        layout_ui_panel.addWidget(btn_generate_exmaple)
        layout_ui_panel.addWidget(btn_clear_all)

        # --- Layout Info ---
        layout_ui_panel.addSpacing(30)
        self.label_layout_info = InvisableLable("LAYOUT INFO")
        layout_ui_panel.addWidget(self.label_layout_info)
        self.lable_i_num_lable = QLabel("Items in layer: N/D")
        self.lable_layers_num = QLabel("Layers can be placed: N/D")
        self.lable_layouts = QLabel("LAYOUTS")
        self.lable_layouts.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_ui_panel.addWidget(self.lable_i_num_lable)
        layout_ui_panel.addWidget(self.lable_layers_num)
        layout_ui_panel.addSpacing(15)
        layout_ui_panel.addWidget(self.lable_layouts)

        # --- Layouts buttons ---
        switch_layout_btns = QHBoxLayout()
        btn_switch_layout_1 = self.create_btn_switch_layout(1)
        btn_switch_layout_2 = self.create_btn_switch_layout(2)
        self.btns_layouts = [btn_switch_layout_1, btn_switch_layout_2]
        switch_layout_btns.addWidget(btn_switch_layout_1)
        switch_layout_btns.addWidget(btn_switch_layout_2)
        layout_ui_panel.addLayout(switch_layout_btns)
        layout_ui_panel.addSpacing(15)

        # --- Item Info ---
        self.label_items_info = CenteredLabel('ITEM INFO')
        layout_ui_panel.addWidget(self.label_items_info)
        # User input field
        layout_item_id = QHBoxLayout()
        self.input_field_item_id = QLineEdit()
        self.input_field_item_id.setPlaceholderText("Enter item's id")
        self.input_field_item_id.textChanged.connect(self.check_item_id)
        self.btn_find_item = QPushButton('Find')
        self.btn_find_item.clicked.connect(self.show_item_info)
        self.btn_find_item.setEnabled(False)
        layout_item_id.addWidget(self.input_field_item_id)
        layout_item_id.addWidget(self.btn_find_item)
        layout_ui_panel.addLayout(layout_item_id)
        layout_ui_panel.addSpacing(5)

        # Item position and rotation
        self.label_item_pos_x = InvisableLable("X: N/D")
        self.label_item_pos_y = InvisableLable("Y: N/D")
        self.label_item_pos_z = InvisableLable("Z: N/D")
        self.label_item_rotation_a = InvisableLable("A: N/D")
        layout_ui_panel.addWidget(self.label_item_pos_x)
        layout_ui_panel.addWidget(self.label_item_pos_y)
        layout_ui_panel.addWidget(self.label_item_pos_z)
        layout_ui_panel.addWidget(self.label_item_rotation_a)

        layout_ui_panel.addStretch()

        # --- Setting up Canvas ---
        self.graphics_view = ZoomableGraphicsView()
        self.graphic_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphic_scene)
        self.graphics_view.setStyleSheet('background-color: rgb(5,5,5)')
        self.graphics_view.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.graphics_view.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        layout_main.addWidget(self.ui_panel_container)
        layout_main.addWidget(self.graphics_view)

        self.setCentralWidget(main_container)

    # ================ CLI Input Handling ================
    def handle_input(self, u_input:str):
        args = u_input.split(' ')
        if args[0].isspace() or args[0] == '':
            print("command:", end=' ')    
            return
        match args[0]:
            case 'lay':
                if self.items_layouts == None:
                    print(f'Create a layout in qt interface first') 
                    return
                if args.__len__() < 2:
                    print(f"Invalid command! Expects: 'lay <number>'")
                    return
                try:
                    self.cli_layout_ind = int(args[1])
                    if self.cli_layout_ind > 0 and self.cli_layout_ind <= self.items_layouts.__len__():
                        print(f"Layout '{self.cli_layout_ind}' selected.")
                    else:
                        print(f"Invalid input! Value shold bigger than 0 and less than amount of layouts ({self.items_layouts.__len__()}).")
                except:
                    print(f"Invalid input! '{args[1]}' should be a number")
            case 'item':
                if self.items_layouts == None:
                    print(f'Create a layout in qt interface first') 
                    return
                if args.__len__() < 2:
                    print(f"Invalid command! Expects: 'item <number>'")
                    return
                if self.cli_layout_ind == -1:
                    print(f"Select a layout via 'sol 1' or 'sol 2' if there are 2 layouts") 
                    return
                try:
                    cli_i_ind = int(args[1])
                    items = self.items_layouts[self.cli_layout_ind].items
                    if cli_i_ind < 0 or cli_i_ind > items.__len__():
                        cli_i_ind -= 1
                        print(f"Invalid input! Value shold bigger than 0 and less than amount of items in layout ({items.__len__()}).")
                    else:
                        print("========= ITEM INFO =========")
                        print(f"Item {cli_i_ind}")
                        print(f"X: {items[cli_i_ind].pos_x}")
                        print(f"Y: {items[cli_i_ind].pos_y}")
                        print(f"Z: {items[cli_i_ind].pos_z}")
                        print(f"A: {items[cli_i_ind].rot_z}")
                except:
                    print(f"Invalid input! '{args[1]}' should be a number")
            case 'clear':
                clear_console()
            case 'help':
                print('========= HELP =========')
                print('For now cli can only give info about an item. To do that you need:')
                print('1. Create a layouts via qt interface')
                print("2. Select a layout via 'lay <layout number>'")
                print("3. Show info of an item via 'item <layout number>'")
            case 'exit':
                sys.exit()
            case _:
                print(f"Unknown command '{args[0]}'")
        print("command: ", end=' ')

    # ================ Application Inititalization ================
    def __init__(self):
        super().__init__()
        # --- Setting up the window --- 
        screen = QGuiApplication.primaryScreen()
        self.setFixedSize(QSize(screen.size().width(), screen.size().height()))
        self.setWindowTitle("ItemsPlacer QT6")
        self.setStyleSheet("background-color: rgb(18, 18, 18)")
        self.u_data = UserData()
        self.items_layouts:list[Layout]
        self.btns_layouts:list[QPushButton]
        self.cli_layout_ind:int

        self.init_ui()

        self.input_thread = InputThread()
        self.input_thread.input_recieved.connect(self.handle_input)
        self.input_thread.start()

        # --- Test only ---
        self.btn_generate_exmaple_logic()
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()