import sys
from Core.main import calc
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtGui import QGuiApplication, QBrush, QPen


class MainWindow(QMainWindow):
    def init_ui(self):
        self.p_height = 0
        self.p_lenght = 0
        self.p_widht = 0
        self.i_height = 0
        self.i_lenght = 0
        self.i_widht = 0
        self.max_height = 0

        # Dividing screen to UI panel and Canvas

        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_container.setLayout(main_layout)

        self.ui_container_widget = QWidget()
        self.ui_container_widget.setFixedWidth(250)

        ui_panel_layout = QVBoxLayout()
        self.ui_container_widget.setLayout(ui_panel_layout)
        self.ui_container_widget.setStyleSheet("background-color: rgb(40, 40, 40)")

        # --- Filling UI Panel ---

        pallet_prop_label = QLabel("PALLETE PROPERTIES")
        pallet_prop_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ui_panel_layout.addWidget(pallet_prop_label)
        # Pallet lenght field
        pallet_l_field = QHBoxLayout()
        pallet_l_field.addWidget(QLabel("Lenght: "))
        pallet_l_field.addWidget(QLineEdit())
        ui_panel_layout.addLayout(pallet_l_field)
        # Pallet width field
        pallet_width_layout = QHBoxLayout()
        pallet_width_layout.addWidget(QLabel("Width: "))
        pallet_width_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(pallet_width_layout)
        # Pallet heigh field
        pallet_height_layout = QHBoxLayout()
        pallet_height_layout.addWidget(QLabel("Height: "))
        pallet_height_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(pallet_height_layout)

        ui_panel_layout.addSpacing(30)

        item_prop_label = QLabel("ITEM PROPERTIES")
        item_prop_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ui_panel_layout.addWidget(item_prop_label)
        # Item lenght field
        item_lenght_layout = QHBoxLayout()
        item_lenght_layout.addWidget(QLabel("Lenght: "))
        item_lenght_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(item_lenght_layout)
        # Item width field
        item_widht_layout = QHBoxLayout()
        item_widht_layout.addWidget(QLabel("Width: "))
        item_widht_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(item_widht_layout)
        # Item height field
        item_height_layout = QHBoxLayout()
        item_height_layout.addWidget(QLabel("Height: "))
        item_height_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(item_height_layout)

        ui_panel_layout.addSpacing(30)

        additional_prop_label = QLabel("ADDITIONAL PROPERTIES")
        additional_prop_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ui_panel_layout.addWidget(additional_prop_label)
        # Max height field
        max_height_layout = QHBoxLayout()
        max_height_layout.addWidget(QLabel("Max height: "))
        max_height_layout.addWidget(QLineEdit())
        ui_panel_layout.addLayout(max_height_layout)

        ui_panel_layout.addSpacing(30)
        
        ui_panel_layout.addWidget(QPushButton("Generate pattern"))
        ui_panel_layout.addStretch()

        # --- Setting up Canvas ---
        self.graphics_view = QGraphicsView()
        self.graphic_scene = QGraphicsScene()

        rect_item = QGraphicsRectItem(0, 0, 300, 50)
        rect_item.setPos(100,100)

        brush = QBrush(Qt.GlobalColor.red)
        pen = QPen(Qt.GlobalColor.white)
        pen.setWidth(1)

        rect_item.setBrush(brush)
        rect_item.setPen(pen)

        self.graphic_scene.addItem(rect_item)
        self.graphics_view.setScene(self.graphic_scene)
        self.graphics_view.setStyleSheet("background-color: rgb(5,5,5)")

        main_layout.addWidget(self.ui_container_widget)
        main_layout.addWidget(self.graphics_view)

        self.setCentralWidget(main_container)

        self.pallet_height_input_field = QWidget()

    def __init__(self):
        super().__init__()
        self.init_ui()
        # Setting up the window        
        screen = QGuiApplication.primaryScreen()
        self.setFixedSize(QSize(screen.size().width(), screen.size().height()))

        self.setWindowTitle("ItemsPlacer QT6")
        self.setStyleSheet("background-color: rgb(18, 18, 18)")
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()