from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from gui_utils.readConstantFile import readConstants
import os

class RunBtnControlWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Run Simulation Dialog")
        self.resize(600,400)
        self.setUpCentralWidget()

    def setUpCentralWidget(self):
        centralWidget = QWidget()
        layout = self.setUpScrollArea()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def setUpScrollArea(self):
        mainLayout = QVBoxLayout()
        self.scroll = QScrollArea()

        contentWidget = QWidget()
        layout = self.setUpLayout()
        contentWidget.setLayout(layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contentWidget)

        btnLayout = self.setButtonLayout()

        mainLayout.addWidget(self.scroll)
        mainLayout.addLayout(btnLayout)
        return mainLayout

    def setUpLayout(self):
        mainLayout = QVBoxLayout()
        splitLayout = QHBoxLayout()

        constant = readConstants()
        self.constantLineEdit = {}

        leftLayout = QFormLayout()
        rightLayout = QFormLayout()

        for i, (key, values) in enumerate(constant.items()):
            if i <= len(constant) // 2: 
                self.setPanelValues(key, values)
                leftLayout.addRow(QLabel(key),self.constantLineEdit[key])
            else:
                self.setPanelValues(key, values)
                rightLayout.addRow(QLabel(key),self.constantLineEdit[key])
        splitLayout.addLayout(leftLayout)
        splitLayout.addLayout(rightLayout)

        mainLayout.addLayout(splitLayout)
        return mainLayout
    
    def setPanelValues(self, key, values):
        if key != 'file_path':
            self.constantLineEdit[key] = QLineEdit()
            self.constantLineEdit[key].setText(str(values))
        else:
            self.constantLineEdit[key] = QComboBox()
            filePath = 'data'
            self.fileList = os.listdir(filePath)
            for file in self.fileList:
                self.constantLineEdit[key].addItem(file)
            for i, file in enumerate(self.fileList):
                self.fileList[i] = os.path.join(filePath, file)
        self.constantLineEdit[key].setFixedHeight(30)


    def setButtonLayout(self):
        self.cancelBtn = QPushButton('Cancel')
        self.runBtn = QPushButton('Start')
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.cancelBtn)
        hLayout.addWidget(self.runBtn)
        return hLayout

        