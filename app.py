from Core import placer
from UI.qt_ui import qt_ui as ui

window = ui.init_ui()
result:str = "NO data"
try:
    result = placer.calc(10, 10, 6, 5,  4,  5,10)
except ValueError as err:
    print("Error")
    window.label.setText(f"error: {err}")

print("NO error")
window.label.setText(f"result: {result}")

