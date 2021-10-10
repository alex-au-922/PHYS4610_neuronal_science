from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from gui_utils.guiComponents import ProgressBar
import sys

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Testing')
        self.progress = ProgressBar('Hello','testing', 100)
        self.btn = QPushButton('Clicks')
        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)
        self.btn.clicked.connect(self.progress.show)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
