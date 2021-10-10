from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from view.demgraph import GraphWidget
from view.widgets import UtilWidget
from view.menu import MenuWidget
from view.runBtnPanel import RunBtnControlWindow
from view.plotBtnPanel import PlotBtnControlWindow
from gui_utils.guiComponents import QVSeperationLine

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.graphWidgets = GraphWidget(self)
        self.utilWidgets = UtilWidget(self)
        self.menuBarWidgets = MenuWidget(self)
        self.runBtnPanel = RunBtnControlWindow(self)
        self.plotBtnPanel = PlotBtnControlWindow(self)
        
        self.setWindowTitle("Izhikevich Model Run")
        self.resize(1280,720)

        self.setUpUI()
    def setUpUI(self):
        centralWidget = QWidget()
        layout = self.setUpLayout()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def setUpLayout(self):
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.graphWidgets,2)
        vSeparateLine = QVSeperationLine()
        mainLayout.addWidget(vSeparateLine)
        mainLayout.addLayout(self.utilWidgets.layout,1)
        return mainLayout
    
    


