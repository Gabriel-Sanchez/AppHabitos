from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QDrag

class DraggableButton(QPushButton):
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(Qt.MoveAction)

class DropArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setLayout(QVBoxLayout())
        self.buttons = []

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        button = e.source()
        index = self.layout().indexOf(button)
        self.layout().removeWidget(button)
        drop_index = self.getDropIndex(e.pos())
        self.layout().insertWidget(drop_index, button)

    def getDropIndex(self, pos):
        for i in range(self.layout().count()):
            if self.layout().itemAt(i).widget().frameGeometry().contains(pos):
                return i
        return self.layout().count()

app = QApplication([])
dropArea = DropArea()
for i in range(10):
    button = DraggableButton(f'Button {i}')
    dropArea.layout().addWidget(button)
dropArea.show()
app.exec_()
