from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class GraphWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.searchGraphBtnList = []
        self.setUpCentralWidget()
    
    def setUpCentralWidget(self):
        self.tabWidget = QTabWidget()
        self.setInitialTabUI()
        self.tabWidget.setTabsClosable(True)
        self.setCentralWidget(self.tabWidget)
    
    def setInitialTabUI(self):
        self.tabWidget.setUpdatesEnabled(True)

        initialTab = TabContent(self.tabWidget)
        self.searchGraphBtnList.append([initialTab,False, None])

        self.tabWidget.insertTab(0,initialTab, "Blank" )
        self.tabWidget.insertTab(1,QWidget(),'+') 
        qlabel = QLabel('')
        qlabel.setFixedSize(0,0)
        self.tabWidget.tabBar().setTabButton(self.tabWidget.count()-1, QTabBar.RightSide, qlabel)

    def setTabInitialView(self):
        return TabContent(self.tabWidget)

class TabContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUpLayout()
    
    def setUpLayout(self):
        self.layout = QVBoxLayout()
        self.setUpWidget()
        self.layout.addWidget(self.searchBtn)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setLayout(self.layout)

    def setUpWidget(self):
        self.searchBtn = QPushButton("Search graphs")

