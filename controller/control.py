from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class Controller:
    def __init__(self, view):
        self.view = view
        self.tabConnectAction()
    
    def tabConnectAction(self):
        self.view.graphWidgets.tabWidget.currentChanged.connect(self.addTabWidget) 
        self.view.graphWidgets.tabWidget.tabCloseRequested.connect(self.closeTabWidget)
    
    def addTabWidget(self, index):
        if index == self.view.graphWidgets.tabWidget.count()-1:
            initialTab = self.view.graphWidgets.setTabInitialView()
            self.view.graphWidgets.tabWidget.insertTab(index, initialTab, "Blank") 
            self.view.graphWidgets.tabWidget.setCurrentIndex(index)
    
    def closeTabWidget(self,index):
        if index == 0 and self.view.graphWidgets.tabWidget.count() == 2:
            initialTab = self.view.graphWidgets.setTabInitialView()
            self.view.graphWidgets.tabWidget.insertTab(index, initialTab, "Blank") 
            self.view.graphWidgets.tabWidget.setCurrentIndex(index)
            self.view.graphWidgets.tabWidget.removeTab(index+1)

        elif index == self.view.graphWidgets.tabWidget.count()-2:
            self.view.graphWidgets.tabWidget.setCurrentIndex(index - 1)
            self.view.graphWidgets.tabWidget.removeTab(index)
        else:
            self.view.graphWidgets.tabWidget.removeTab(index)
    

    def viewConnectAction(self):
        pass