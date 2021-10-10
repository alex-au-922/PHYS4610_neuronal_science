from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from main import MainExecution
from gui_utils.guiComponents import ProgressBar, showCompleted
from utils.runNotification import sendNotification
from utils.checkFunctions import checkSearchPathConstantFile
import sys
import os
import yaml

class Controller:
    def __init__(self, view):
        self.view = view
        self.threadPool = QThreadPool()
        self.runBtnConnection()
        self.plotBtnConnection()
        self.tabConnectAction()
    
    def runBtnConnection(self):
        self.view.utilWidgets.trainBtn.clicked.connect(self.view.runBtnPanel.show)
        self.view.runBtnPanel.cancelBtn.clicked.connect(self.view.runBtnPanel.close)
        self.view.runBtnPanel.runBtn.clicked.connect(self.runBtnStartConnection)
    
    def runBtnStartConnection(self):
        self.runBtnStartGetConstants()
        self.view.runBtnPanel.close()
        self.mainExecution = MainExecution(self.runSimArgs)
        self.progress = ProgressBar('Running Simulation', 'Initializing...', self.mainExecution.total_time_step, self.view)
        self.mainExecution.signal.progress.connect(self.progress.updateVal)
        self.mainExecution.signal.plotting.connect(lambda: self.progress.setNoLengthMode('Plot Graph',' Plotting...'))
        self.mainExecution.signal.finished.connect(self.progress.close)
        self.mainExecution.signal.finished.connect(lambda: showCompleted('Success', 'The simulation has completed.', self.view))
        self.mainExecution.signal.finished.connect(lambda: sendNotification('Izhikevich Model Simulation', 'Simulation Completed'))
        self.progress.show()
        self.mainExecution.initialization()
        self.mainExecution.start()

    def runBtnStartGetConstants(self):
        buffConstants = {}
        for key, widget in self.view.runBtnPanel.constantLineEdit.items():
            if key == 'file_path':
                value = self.view.runBtnPanel.fileList[widget.currentIndex()]
            else:
                value = eval(widget.text())
            buffConstants[key] = value
        
        inhibitDict = {}
        excitedDict = {}
        runConstants = {}
        for key, value in buffConstants.items():
            if 'INHIBIT_' in key:
                inhibitDict[key.replace('INHIBIT_','')] = value
            elif 'EXCITED_' in key:
                excitedDict[key.replace('EXCITED_','')] = value
            else:
                runConstants[key] = value
        runConstants['INHIBIT'] = inhibitDict
        runConstants['EXCITED'] = excitedDict
        
        with open('constants.yaml') as stream:
            self.runSimArgs = yaml.safe_load(stream)
        
        for key, value in self.runSimArgs.items():
            if isinstance(value, dict):
                for innerKey, innerValue in value.items():
                    if innerKey in ['INHIBIT', 'EXCITED']:
                        for innerMostKey, _ in innerValue.items():
                            self.runSimArgs[key][innerKey][innerMostKey] = runConstants[innerKey][innerMostKey]
                    elif innerKey in runConstants:
                        self.runSimArgs[key][innerKey] = runConstants[innerKey]
            else:
                if key in runConstants:
                    self.runSimArgs[key] = runConstants[key]

    def plotBtnConnection(self):
        self.view.utilWidgets.plotBtn.clicked.connect(self.view.plotBtnPanel.show)
        self.plotBtnCancelConnection()
        self.plotBtnPlotConnection()
    
    def plotBtnCancelConnection(self):
        self.view.plotBtnPanel.cancelBtn.clicked.connect(self.view.plotBtnPanel.close)
    
    def plotBtnPlotConnection(self):
        pass

    def tabConnectAction(self):
        self.view.graphWidgets.tabWidget.currentChanged.connect(self.changeTabWidget) 
        self.view.graphWidgets.tabWidget.tabCloseRequested.connect(self.closeTabWidget)
        
        for widget, _,_ in self.view.graphWidgets.searchGraphBtnList:
            widget.searchBtn.clicked.connect(self.searchGraphAction)
    
    def changeTabWidget(self, index):
        if index == self.view.graphWidgets.tabWidget.count()-1:
            initialTab = self.view.graphWidgets.setTabInitialView()
            initialTab.searchBtn.clicked.connect(lambda: self.searchGraphAction(index))
            self.view.graphWidgets.searchGraphBtnList.append([initialTab, False, None])
            self.view.graphWidgets.tabWidget.insertTab(index, initialTab, "Blank") 
            self.view.graphWidgets.tabWidget.setCurrentIndex(index)
            self.view.utilWidgets.refreshTable()
        else:
            if not self.view.graphWidgets.searchGraphBtnList[index][1]:
                self.view.utilWidgets.refreshTable()
            else:
                self.view.utilWidgets.refreshTable(os.path.join(self.view.graphWidgets.searchGraphBtnList[index][2], 'result_constants.yaml'))

    
    def closeTabWidget(self,index):
        if index == 0 and self.view.graphWidgets.tabWidget.count() == 2:
            initialTab = self.view.graphWidgets.setTabInitialView()
            initialTab.searchBtn.clicked.connect(lambda: self.searchGraphAction(index))
            self.view.graphWidgets.searchGraphBtnList.insert(0,initialTab)
            self.view.graphWidgets.tabWidget.insertTab(index, initialTab, "Blank") 
            self.view.graphWidgets.tabWidget.setCurrentIndex(index)
            self.view.utilWidgets.refreshTable()
            self.view.graphWidgets.tabWidget.removeTab(index+1)
            del self.view.graphWidgets.searchGraphBtnList[index+1]

        else:
            if self.view.graphWidgets.tabWidget.currentIndex() > index:
                self.view.graphWidgets.tabWidget.setCurrentIndex(self.view.graphWidgets.tabWidget.currentIndex())
            elif self.view.graphWidgets.tabWidget.currentIndex()  == index:
                if self.view.graphWidgets.tabWidget.count()-2 == index:
                    self.view.graphWidgets.tabWidget.setCurrentIndex(self.view.graphWidgets.tabWidget.currentIndex() - 1)
            else:
                self.view.graphWidgets.tabWidget.setCurrentIndex(self.view.graphWidgets.tabWidget.currentIndex())
            self.view.graphWidgets.tabWidget.removeTab(index)
            del self.view.graphWidgets.searchGraphBtnList[index]
            for widget, boolean, basePath in self.view.graphWidgets.searchGraphBtnList:
                if boolean:
                    self.refreshTableForGraph(basePath)
                else:
                    self.view.utilWidgets.refreshTable()

    def searchGraphAction(self, index):
        folderSearch = QFileDialog()
        folderSearch.setFileMode(QFileDialog.AnyFile)
        path = os.getcwd()
        filterType = "Images (*.jpg *.jpeg)"
        file = folderSearch.getOpenFileName(directory=path, filter=filterType)
        folderSearch.show()
        basePath, fileName = os.path.split(file[0])
        if checkSearchPathConstantFile(basePath, self.view):
            self.refreshTabUI(basePath, fileName, index)
    
    def refreshTabUI(self, basePath, fileName, index):
        print(self.view.graphWidgets.searchGraphBtnList, index)
        pic = QLabel(self.view.graphWidgets.tabWidget)
        pic.setPixmap(QPixmap(os.path.join(basePath,fileName)))
        btn = self.view.graphWidgets.searchGraphBtnList[index][0].layout.itemAt(0)
        btn.widget().deleteLater()
        self.view.graphWidgets.searchGraphBtnList[index][0].layout.addWidget(pic)
        self.view.graphWidgets.searchGraphBtnList[index][1] = True
        self.view.graphWidgets.searchGraphBtnList[index][2] = basePath 
        self.refreshTabTitle(basePath, fileName, index)
        self.refreshTableForGraph(basePath)

    def refreshTableForGraph(self, basePath):
        self.view.utilWidgets.refreshTable(os.path.join(basePath, 'result_constants.yaml'))
    
    def refreshTabTitle(self, basePath, fileName, index):
        name = 'Fire' if fileName == 'firing_rate.jpg' else 'ISI' if fileName == 'log_spike_interval.jpg' else 'Raster'
        _, param = os.path.split(basePath)
        dt, timeStep = param.split('_')
        self.view.graphWidgets.tabWidget.setTabText(index,f'{name} ({dt},{timeStep})')