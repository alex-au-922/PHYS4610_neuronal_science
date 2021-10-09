from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class GraphWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUpCentralWidget()
    
    def setUpCentralWidget(self):
        self.tabWidget = QTabWidget()
        self.setInitialTabUI()
        self.tabWidget.setTabsClosable(True)
        self.setCentralWidget(self.tabWidget)
    
    def setInitialTabUI(self):
        self.tabWidget.setUpdatesEnabled(True)

        initialTab =self.setTabInitialView()

        self.tabWidget.insertTab(0,initialTab, "Blank" )
        self.tabWidget.insertTab(1,QWidget(),'+') 
        qlabel = QLabel('')
        qlabel.setFixedSize(0,0)
        self.tabWidget.tabBar().setTabButton(self.tabWidget.count()-1, QTabBar.RightSide, qlabel)

    def setTabInitialView(self):
        initialTab = QWidget()
        layout = QVBoxLayout()
        initialSearchBtn = QPushButton("Search graphs")
        layout.addWidget(initialSearchBtn)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        initialTab.setLayout(layout)
        return initialTab