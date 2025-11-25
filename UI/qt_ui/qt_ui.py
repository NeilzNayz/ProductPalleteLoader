import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class QT_Window:
    def __init__(self, app:QApplication) -> None:
        self.screen_size = app.primaryScreen().size()
        self.window = QWidget()
        self.window.setWindowTitle("Testing QT")
        self.window.setGeometry(
            100,
            0,
            self.screen_size.width(),
            self.screen_size.height())
        
        self.label = QLabel("Hello",self.window)
        self.label.setFont(QFont("Arial",60))
        self.label.setGeometry(0,0, 500, 200)
        self.label.setStyleSheet("color: #040026;" \
                                 "background-color: #00c7c7;" \
                                 "font-weight: bold;" \
                                 "font-style:italic;" \
                                 "text-decoration: underline")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

def init_ui() -> QT_Window:
    app = QApplication(sys.argv)
    qt_window = QT_Window(app)
    qt_window.window.show()
    sys.exit(app.exec())
    return qt_window

if __name__ == "__main__":
    init_ui()