import sys
from Core.models import UserData, Solution
from Core.main import generate_solutions
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtGui import QGuiApplication, QWheelEvent, QBrush, QPen
from PyQt6 import QtWidgets, QtGui, QtCore

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

    def create_lable_widget(self, lable_text):
        lable = QLabel(lable_text)
        lable.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        return lable
    
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
        
    def create_field_layout(self, name, field_var_name):
        field_layout = QHBoxLayout()
        field_lable = QLabel(f"{name}: ")
        field_line_edit = QLineEdit()
        field_line_edit.textChanged.connect(lambda text: self.check_field_value(text, field_var_name, field_lable))
        field_layout.addWidget(field_lable)
        field_layout.addWidget(field_line_edit)
        return field_layout
    
    def visualize_solutions(self, solutions:list[Solution]):
        print("Visualizing..............")
        solution = solutions[0]
        for item in solution.items:
            print(f'item info pos: x{item.pos_x} y{item.pos_y}  size: w{item.width} h{item.lenght}  orientation: {item.orientation}')
            rect_item = QGraphicsRectItem(item.pos_x, self.user_data.p_lenght - item.lenght - item.pos_y, item.width, item.lenght)
            brush = QBrush(Qt.GlobalColor.red)
            pen = QPen(Qt.GlobalColor.white)
            pen.setWidth(1)
            rect_item.setBrush(brush)
            rect_item.setPen(pen)
            self.graphic_scene.addItem(rect_item)

    def generate(self):
        try:
            if self.user_data.is_p_height_correct == True and \
            self.user_data.is_p_lenght_correct == True and \
            self.user_data.is_p_width_correct  == True and \
            self.user_data.is_i_height_correct == True and \
            self.user_data.is_i_lenght_correct == True and \
            self.user_data.is_i_width_correct  == True and \
            self.user_data.is_max_height_correct == True:
                self.visualize_solutions(generate_solutions(self.user_data))
        except Exception as err:
            print(f'Error while generating: {err}')

    def init_ui(self):
        # --- Creating conrainers ---
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_container.setLayout(main_layout)

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
        generate_button.pressed.connect(self.generate)
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