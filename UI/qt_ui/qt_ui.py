import sys
from Core.models import UserData, Solution, Item, Orientation
from Core.main import generate_solutions
from PyQt6.QtWidgets import QApplication, QGraphicsTextItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtGui import QGuiApplication, QWheelEvent, QBrush, QPen, QColor
from PyQt6 import QtWidgets

class ProductItem(QGraphicsRectItem):
    def __init__(self, item:Item, user_data:UserData, user_or:Orientation) -> None:
        i_w = item.width if item.orientation == user_or else item.lenght
        i_l = item.lenght if item.orientation == user_or else item.width
        super().__init__(0,0, i_w, i_l)
        self.setPos(item.pos_x - i_w / 2, user_data.p_l - i_l / 2 - item.pos_y)

        # --- Creating Item rectangle ---
        brush = QBrush(Qt.GlobalColor.transparent)
        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(1)
        self.setBrush(brush)
        self.setPen(pen)
        
        # --- Adding central point ---
        r = min(i_l,i_w) * 0.07
        i_mid_x = i_w / 2 - r
        i_mid_y = i_l / 2 - r
        circle = QGraphicsEllipseItem(0,0, r * 2,r * 2)
        circle.setBrush(QBrush(Qt.GlobalColor.transparent))
        circle.setPen(QPen(Qt.GlobalColor.red))
        circle.setPos(i_mid_x,i_mid_y)
        circle.setParentItem(self)

        id_lable = QGraphicsTextItem(str(item.id), self)
        id_lable.setPos(i_mid_x - r, i_mid_y + r)

# Zoomable QGraphicsView
class ZoomableGraphicsView(QtWidgets.QGraphicsView):
    SCALE_FACTOR = 1.1
    def wheelEvent(self, event: QWheelEvent | None) -> None:
        if event.angleDelta().y() > 0:
            self.scale(self.SCALE_FACTOR, self.SCALE_FACTOR)
        else:
            factor = 1 / self.SCALE_FACTOR
            self.scale(factor, factor)

class MainWindow(QMainWindow):
    SIZE_MULTIPLAYER = 1

    def create_lable_widget(self, lable_text):
        lable = QLabel(lable_text)
        lable.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        return lable
    
    def check_field_value(self, text:str, field_var_name:str, field_lable:QLabel):
        if text.isspace() or text == '':
            setattr(self.u_data, f'{field_var_name}', 0)
            field_lable.setStyleSheet("color: white")
            self.generate_button.setEnabled(False)
            return
        try:
            setattr(self.u_data, field_var_name, float(text) * self.SIZE_MULTIPLAYER)
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
    
    def visualize_solution(self, solution:Solution):
        # Visualizing pallete
        self.graphic_scene.clear()
        pallet = QGraphicsRectItem(0, 0, self.u_data.p_w, self.u_data.p_l)
        pallet.setBrush(QBrush(Qt.GlobalColor.transparent))
        pallet.setPen(QPen(QColor('brown')))
        self.graphic_scene.addItem(pallet)

        # Visualizing items
        for i in solution.items:
            print(f'item info pos: x{i.pos_x} y{i.pos_y}  size: w{i.width} l{i.lenght}  orientation: {i.orientation}')
            rect_i = ProductItem(i, self.u_data, solution.user_or)
            self.graphic_scene.addItem(rect_i)

    def btn_generate_logic(self):
        self.solutions = generate_solutions(self.u_data)
        self.visualize_solution(self.solutions[0])
        self.solutions_num_lable.setText(f'Solutions found: {self.solutions.__len__()}')
        self.i_num_lable.setText(f'Items loaded: {self.solutions[0].max_i}')
        self.layers_num_lable.setText(f'Layers can be placed: {(self.u_data.max_h - self.u_data.p_h) / self.u_data.i_h}')
        self.solutions_num_lable.setVisible(True)
        self.i_num_lable.setVisible(True)
        self.layers_num_lable.setVisible(True)

    def init_ui(self):
        """Initializes left ui panel, canvas, etc"""
        # --- Creating conrainers ---
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_container.setLayout(main_layout)

        self.solutions:list[Solution]
        self.field_inputs:list[QLineEdit] = []
        self.ui_panel_container = QWidget()
        self.ui_panel_container.setFixedWidth(250)
        ui_panel_layout = QVBoxLayout()
        self.ui_panel_container.setLayout(ui_panel_layout)
        self.ui_panel_container.setStyleSheet('background-color: rgb(40, 40, 40)')

        # --- Filling UI Panel ---
        ui_panel_layout.addWidget(self.create_lable_widget('PALLETE PROPERTIES'))
        ui_panel_layout.addLayout(self.create_field_layout('Lenght', 'p_l'))
        ui_panel_layout.addLayout(self.create_field_layout('Width',  'p_w' ))
        ui_panel_layout.addLayout(self.create_field_layout('Height', 'p_h'))
        ui_panel_layout.addSpacing(30)
        ui_panel_layout.addWidget(self.create_lable_widget("ITEM PROPERTIES"))
        ui_panel_layout.addLayout(self.create_field_layout('Lenght', 'i_l'))
        ui_panel_layout.addLayout(self.create_field_layout('Width',  'i_w' ))
        ui_panel_layout.addLayout(self.create_field_layout('Height', 'i_h'))
        ui_panel_layout.addSpacing(30)
        ui_panel_layout.addWidget(self.create_lable_widget('ADDITIONAL PROPERTIES'))
        ui_panel_layout.addLayout(self.create_field_layout('Max height', 'max_h'))
        ui_panel_layout.addSpacing(30)
        self.generate_button = QPushButton('Generate pattern')
        self.generate_button.pressed.connect(self.btn_generate_logic)
        self.generate_button.setEnabled(False)
        ui_panel_layout.addWidget(self.generate_button)

        # --- Solution Info ---
        ui_panel_layout.addSpacing(50)
        ui_panel_layout.addWidget(self.create_lable_widget("Solution Info"))
        self.solutions_num_lable = QLabel("Solutions found: XXX")
        self.i_num_lable = QLabel("Items in layer: XXX")
        self.layers_num_lable = QLabel("Layers can be placed: XXX")
        self.i_num_lable.setVisible(False)
        self.layers_num_lable.setVisible(False)
        self.solutions_num_lable.setVisible(False)
        ui_panel_layout.addWidget(self.solutions_num_lable)
        ui_panel_layout.addWidget(self.i_num_lable)
        ui_panel_layout.addWidget(self.layers_num_lable)
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
        # --- Setting up the window --- 
        screen = QGuiApplication.primaryScreen()
        self.setFixedSize(QSize(screen.size().width(), screen.size().height()))
        self.setWindowTitle("ItemsPlacer QT6")
        self.setStyleSheet("background-color: rgb(18, 18, 18)")
        self.u_data = UserData()

        self.init_ui()

        # --- Test only ---
        self.field_inputs[0].setText(str(15.2))
        self.field_inputs[1].setText(str(10.2))
        self.field_inputs[2].setText(str(1))
        self.field_inputs[3].setText(str(6))
        self.field_inputs[4].setText(str(2.7))
        self.field_inputs[5].setText(str(1))
        self.field_inputs[6].setText(str(12))
        self.btn_generate_logic()
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()