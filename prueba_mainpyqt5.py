from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 300, 300, 300)
    win.setWindowTitle("With Tim!")
    win.show()
    sys.exit(app.exec_())

window()
