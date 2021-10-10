from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from gui_utils.guiComponents import QHSeperationLine
import os

class PlotBtnControlWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plot Graph Dialog")
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
        folderLayout = self.setFolderLineEditLayout()
        firePlotLayout = self.setFirePlotLayout()
        ISIPlotLayout = self.setISIPlotLayout()
        rasterPlotLayout = self.setRasterPlotLayout()
        hSeparator1 = QHSeperationLine(self.parent())
        hSeparator2 = QHSeperationLine(self.parent())
        hSeparator3 = QHSeperationLine(self.parent())

        mainLayout.addLayout(folderLayout)
        mainLayout.addWidget(hSeparator1)

        mainLayout.addLayout(firePlotLayout)
        mainLayout.addWidget(hSeparator2)

        mainLayout.addLayout(ISIPlotLayout)
        mainLayout.addWidget(hSeparator3)

        mainLayout.addLayout(rasterPlotLayout)
        return mainLayout
    
    def setFolderLineEditLayout(self):
        layout = QHBoxLayout()

        self.folderLabel = QLabel("Folder:", self.parent())

        self.folderLineEdit = QLineEdit(self.parent())
        self.folderLineEdit.setText(os.getcwd())
    
        self.folderBtn = QPushButton(self.parent())
        self.folderBtn.setFixedSize(30,30)
        self.folderBtn.setIcon(QIcon('./gui_utils/folderSearch.png'))
        layout.addWidget(self.folderLabel)
        layout.addWidget(self.folderLineEdit)
        layout.addWidget(self.folderBtn)

        return layout

    def setFirePlotLayout(self):
        layout = QVBoxLayout()
        editLayout = QFormLayout()
        fireLabel = QLabel('<h4>Firing Frequency Distribution Plot</h4>')
        fireLabel.setFixedHeight(30)
        layout.addWidget(fireLabel)

        self.fireBin = QLineEdit()
        self.fireBin.setText(str(40))

        self.fireWidth = QLineEdit()
        self.fireWidth.setText(str(10))

        self.fireHeight = QLineEdit()
        self.fireHeight.setText(str(6))

        editLayout.addRow('Bin:', self.fireBin)
        editLayout.addRow('Width:', self.fireWidth)
        editLayout.addRow('Height:', self.fireHeight)

        layout.addLayout(editLayout)

        return layout

    def setISIPlotLayout(self):
        layout = QVBoxLayout()
        isiLabel = QLabel('<h4>ISI Distribution Plot</h4>')
        isiLabel.setFixedHeight(30)
        layout.addWidget(isiLabel)

        editLayout = QFormLayout()

        self.isiBin = QLineEdit()
        self.isiBin.setText(str(40))

        self.isiWidth = QLineEdit()
        self.isiWidth.setText(str(10))

        self.isiHeight = QLineEdit()
        self.isiHeight.setText(str(6))

        editLayout.addRow('Bin:', self.isiBin)
        editLayout.addRow('Width:', self.isiWidth)
        editLayout.addRow('Height:', self.isiHeight)
        layout.addLayout(editLayout)
        return layout

    def setRasterPlotLayout(self):
        layout = QVBoxLayout()
        rasterLabel = QLabel('<h4>Raster Plot</h4>')
        rasterLabel.setFixedHeight(30)
        layout.addWidget(rasterLabel)

        editLayout = QFormLayout()

        self.rasterWidth = QLineEdit()
        self.rasterWidth.setText(str(10))

        self.rasterHeight = QLineEdit()
        self.rasterHeight.setText(str(6))

        editLayout.addRow('Width:', self.rasterWidth)
        editLayout.addRow('Height:', self.rasterHeight)
        layout.addLayout(editLayout)

        return layout
    
    def setButtonLayout(self):
        self.cancelBtn = QPushButton('Cancel')
        self.runBtn = QPushButton('Plot')
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.cancelBtn)
        hLayout.addWidget(self.runBtn)
        return hLayout



        