from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import os
from gui_utils.readConstantFile import readConstants
from gui_utils.guiComponents import QHSeperationLine

class UtilWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = self.setUpUtilUI()
    
    def setUpUtilUI(self):
        layout = QVBoxLayout()
        self.setUpWidgets()
        
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.trainBtn)
        btnLayout.addWidget(self.plotBtn)

        folderLayout = QHBoxLayout()
        folderLayout.addWidget(self.folderLabel)
        folderLayout.addWidget(self.folderLineEdit)
        folderLayout.addWidget(self.folderBtn)

        layout.addLayout(btnLayout)
        layout.addLayout(folderLayout)
        hLine = QHSeperationLine()
        layout.addWidget(hLine)
        layout.addWidget(self.paramList)
        return layout

    def setUpWidgets(self):
        self.setUpTrainButton()
        self.setUpPlotButton()
        self.setUpFolderLabel()
        self.setUpFolderLineEdit()
        self.setUpFolderButton()
        self.setUpParamList()
    
    def setUpTrainButton(self):
        self.trainBtn = QPushButton("Run", self.parent())
    
    def setUpPlotButton(self):
        self.plotBtn = QPushButton("Plot", self.parent())   
    
    def setUpFolderLabel(self):
        self.folderLabel = QLabel("Folder:", self.parent())

    def setUpFolderLineEdit(self):
        self.folderLineEdit = QLineEdit(self.parent())
        self.folderLineEdit.setText(os.getcwd())
    
    def setUpFolderButton(self):
        self.folderBtn = QPushButton(self.parent())
        self.folderBtn.setIcon(QIcon('./gui_utils/folderSearch.png'))

    def setUpParamList(self):
        self.paramList = QTableView()

        def createModel():
            tableModel = QStandardItemModel()
            tableModel.setHorizontalHeaderLabels(['Parameter', 'Value'])
            args = readConstants()
            for i, dictionary in enumerate(args.items()):
                for j, value in enumerate(dictionary):
                    item = QStandardItem(str(value))
                    tableModel.setItem(i, j, item)
            return tableModel 

        self.tableModel = createModel()
        self.paramList.setModel(self.tableModel)            
        self.paramList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)