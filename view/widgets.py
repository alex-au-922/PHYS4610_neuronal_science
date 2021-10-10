from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import os
from gui_utils.readConstantFile import readConstants
from gui_utils.guiComponents import QHSeperationLine

class UtilWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tableModel = None
        self.layout = self.setUpUtilUI()
    
    def setUpUtilUI(self):
        layout = QVBoxLayout()
        self.setUpWidgets()
        
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.trainBtn)
        btnLayout.addWidget(self.plotBtn)

        layout.addLayout(btnLayout)
        hLine = QHSeperationLine()
        layout.addWidget(hLine)
        layout.addWidget(self.paramList)
        return layout

    def setUpWidgets(self):
        self.setUpTrainButton()
        self.setUpPlotButton()
        self.setUpParamList()
    
    def setUpTrainButton(self):
        self.trainBtn = QPushButton("Run", self.parent())
    
    def setUpPlotButton(self):
        self.plotBtn = QPushButton("Plot", self.parent())   

    def setUpParamList(self, fileName = None):
        self.paramList = QTableView()
        self.refreshTable()           
        self.paramList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def createModel(self,  fileName):
        tableModel = QStandardItemModel()
        tableModel.setHorizontalHeaderLabels(['Parameter', 'Value'])
        if fileName is not None:
            args = readConstants(fileName)
            for i, dictionary in enumerate(args.items()):
                for j, value in enumerate(dictionary):
                    item = QStandardItem(str(value))
                    tableModel.setItem(i, j, item)
        return tableModel 
    
    def refreshTable(self, fileName = None):
        if self.tableModel is not None:
            self.tableModel.clear()
        self.tableModel = self.createModel(fileName)
        self.paramList.setModel(self.tableModel)
    