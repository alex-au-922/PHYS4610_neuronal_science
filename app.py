from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import sys
from view.ui import MainWindow
from controller.control import Controller

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    control = Controller(window)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
