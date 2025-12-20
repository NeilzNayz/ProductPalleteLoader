import sys
from Core.models import UserData, Solution, Item
from Core.main import generate_solutions
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtGui import QGuiApplication, QWheelEvent, QBrush, QPen
from PyQt6 import QtWidgets, QtGui, QtCore

class ProductItem(QGraphicsRectItem):
    def __init__(self, item:Item, user_data:UserData) -> None:
        super().__init__(0,0, item.width, item.lenght)
        self.setPos(item.pos_x - item.width / 2, user_data.p_lenght - item.lenght / 2 - item.pos_y)
        # --- Creating Item rectangle ---
        brush = QBrush(Qt.GlobalColor.transparent)
        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(1)
        self.setBrush(brush)
        self.setPen(pen)

        r = min(item.height,item.width)/4
        self.circle = QGraphicsEllipseItem(0,0, r * 2,r * 2)
        self.circle.setParentItem(self)
        self.circle.setPos(item.pos_y, item.pos_x)

        self.circle.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.circle.setPen(QPen(Qt.GlobalColor.red))

# Zoomable class that inherited by QGraphicsView
class ZoomableGraphicsView(QtWidgets.QGraphicsView):
    SCALE_FACTOR = 1.1
    def wheelEvent(self, event: QWheelEvent | None) -> None:
        if event.angleDelta().y() > 0:
            self.scale(self.SCALE_FACTOR, self.SCALE_FACTOR)
        else:
            factor = 1 / self.SCALE_FACTOR
            self.scale(factor, factor)

class MainWindow(QMainWindow):

    SIZE_MULTIPLAYER = 20

    # Creates a lable aligned by center
    def create_lable_widget(self, lable_text):
        lable = QLabel(lable_text)
        lable.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        return lable
    
    # Checks if field is empty/spaces or convertable to float 
    def check_field_value(self, text:str, field_var_name:str, field_lable:QLabel):
        if text.isspace() or text == '':
            setattr(self.user_data, f'is_{field_var_name}_correct', False)
            field_lable.setStyleSheet("color: white")
            return
        try:
            setattr(self.user_data, field_var_name, float(text) * self.SIZE_MULTIPLAYER)
            setattr(self.user_data, f'is_{field_var_name}_correct', True)
            field_lable.setStyleSheet("color: rgb(3, 252, 7)")
        except:
            setattr(self.user_data, f'is_{field_var_name}_correct', False)
            field_lable.setStyleSheet("color: red")
        
    # Creates layout that contains variable's field and lable  
    def create_field_layout(self, name, field_var_name):
        field_layout = QHBoxLayout()
        field_lable = QLabel(f"{name}: ")
        field_line_edit = QLineEdit()
        field_line_edit.textChanged.connect(lambda text: self.check_field_value(text, field_var_name, field_lable))
        field_layout.addWidget(field_lable)
        field_layout.addWidget(field_line_edit)
        return field_layout
    
    # Visualizes calculated solution
    def visualize_solution(self, solution:Solution):
        self.graphic_scene.clear()
        pallet = QGraphicsRectItem(0, 0, self.user_data.p_width, self.user_data.p_lenght)
        pallet.setBrush(QBrush(Qt.GlobalColor.transparent))
        pallet.setPen(QPen(Qt.GlobalColor.red))
        self.graphic_scene.addItem(pallet)

        for item in solution.items:
            print(f'item info pos: x{item.pos_x} y{item.pos_y}  size: w{item.width} l{item.lenght}  orientation: {item.orientation}')
            rect_item = ProductItem(item=item, user_data=self.user_data)
            self.graphic_scene.addItem(rect_item)

    # Checks that all values filled correctly. Can throw an Exception in calculating/visualizing proccess
    def btn_generate_logic(self):
        self.user_data.p_height = 1 * self.SIZE_MULTIPLAYER
        self.user_data.p_lenght = 15.2 * self.SIZE_MULTIPLAYER
        self.user_data.p_width = 10.2 * self.SIZE_MULTIPLAYER
        self.user_data.i_height = 1 * self.SIZE_MULTIPLAYER
        self.user_data.i_lenght = 4 * self.SIZE_MULTIPLAYER
        self.user_data.i_width = 2.5 * self.SIZE_MULTIPLAYER
        self.user_data.max_height = 12 * self.SIZE_MULTIPLAYER
        self.solutions = generate_solutions(self.user_data)
        self.visualize_solution(self.solutions[0])
        return
        try:
            if self.user_data.is_p_height_correct == True and \
            self.user_data.is_p_lenght_correct == True and \
            self.user_data.is_p_width_correct  == True and \
            self.user_data.is_i_height_correct == True and \
            self.user_data.is_i_lenght_correct == True and \
            self.user_data.is_i_width_correct  == True and \
            self.user_data.is_max_height_correct == True:
                self.solutions = generate_solutions(self.user_data)
                self.visualize_solution(self.solutions[0])
            else:
                print("Some fields are not filled correctly")
        except Exception as err:
            print(f'Error while generating: {err}')

    # Initalizes left ui panel(buttons, fields and labels) and visualize area(graphics view and graphics scene)
    def init_ui(self):
        # --- Creating conrainers ---
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_container.setLayout(main_layout)

        self.solutions:list[Solution]

        self.ui_panel_container = QWidget()
        self.ui_panel_container.setFixedWidth(250)
        ui_panel_layout = QVBoxLayout()
        self.ui_panel_container.setLayout(ui_panel_layout)
        self.ui_panel_container.setStyleSheet('background-color: rgb(40, 40, 40)')

        # --- Filling UI Panel ---
        ui_panel_layout.addWidget(self.create_lable_widget('PALLETE PROPERTIES'))
        ui_panel_layout.addLayout(self.create_field_layout('Lenght', 'p_lenght'))
        ui_panel_layout.addLayout(self.create_field_layout('Height', 'p_height'))
        ui_panel_layout.addLayout(self.create_field_layout('Width',  'p_width' ))
        ui_panel_layout.addSpacing(30)
        ui_panel_layout.addWidget(self.create_lable_widget("ITEM PROPERTIES"))
        ui_panel_layout.addLayout(self.create_field_layout('Lenght', 'i_lenght'))
        ui_panel_layout.addLayout(self.create_field_layout('Height', 'i_height'))
        ui_panel_layout.addLayout(self.create_field_layout('Width',  'i_width' ))
        ui_panel_layout.addSpacing(30)
        ui_panel_layout.addWidget(self.create_lable_widget('ADDITIONAL PROPERTIES'))
        ui_panel_layout.addLayout(self.create_field_layout('Max height', 'max_height'))
        ui_panel_layout.addSpacing(30)
        generate_button = QPushButton('Generate pattern')
        generate_button.pressed.connect(self.btn_generate_logic)
        ui_panel_layout.addWidget(generate_button)
        ui_panel_layout.addStretch()

        # --- Setting up Canvas ---
        self.graphics_view = ZoomableGraphicsView()
        self.graphic_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphic_scene)
        self.graphics_view.setStyleSheet('background-color: rgb(5,5,5)')
        self.graphics_view.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.graphics_view.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        main_layout.addWidget(self.ui_panel_container)
        main_layout.addWidget(self.graphics_view)

        self.setCentralWidget(main_container)

    def __init__(self):
        super().__init__()
        # Setting up the window        
        screen = QGuiApplication.primaryScreen()
        self.setFixedSize(QSize(screen.size().width(), screen.size().height()))
        self.setWindowTitle("ItemsPlacer QT6")
        self.setStyleSheet("background-color: rgb(18, 18, 18)")

        self.user_data = UserData()

        self.init_ui()  
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()