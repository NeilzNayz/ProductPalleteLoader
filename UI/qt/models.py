from Core.models import Item, UserData
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QBrush, QPen, QWheelEvent
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets

class ProductItem(QGraphicsRectItem):
    def __init__(self, item:Item, user_data:UserData, size_mult:float) -> None:
        i_w = (item.width if item.rot_z == 0 else item.lenght) * size_mult
        i_l = (item.lenght if item.rot_z == 0 else item.width) * size_mult
        super().__init__(0,0, i_w, i_l)
        self.setPos(item.pos_x * size_mult - i_w / 2, user_data.p_l * size_mult - i_l / 2 - item.pos_y * size_mult)

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

class LayoutButton(QPushButton):
    def __init__(self, btn_num:int):
        super().__init__(str(btn_num))
        self.setEnabled(False)
        self.setVisible(False)
        self.setCheckable(True)

class CenteredLabel(QLabel):
    def __init__(self, text:str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

class InvisableLable(QLabel):
    def __init__(self, text:str):
        super().__init__(text)
        self.setVisible(False)