from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class QHSeperationLine(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
    return

class QVSeperationLine(QFrame):
  def __init__(self,parent=None):
    super().__init__(parent)
    self.setFixedWidth(20)
    self.setFrameShape(QFrame.VLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    return
  
class ProgressBar(QProgressDialog):
  def __init__(self,windowTitle, initialText, length,parent=None):
    super().__init__(parent)
    self.length = length
    self.setWindowTitle(windowTitle)
    self.setLabelText(initialText)
    self.setMinimumDuration(1)
    self.setWindowModality(Qt.WindowModal)
    self.setRange(0, length)
  
  def updateVal(self, val, eta, iterRate):
    self.setLabelText(f'Progress: {val} / {self.length}\nETA: {eta}\nIteration Rate: {iterRate:.2f}/s')
    self.setValue(val)
  
  def setNoLengthMode(self, windowTitle, initialText):
    self.setWindowTitle(windowTitle)
    self.setLabelText(initialText)
    self.setRange(0, 0)

class CompleteDialog(QMessageBox):
  def __init__(self,windowTitle, initialText, parent=None):
    super().__init__(parent)
    self.setWindowTitle(windowTitle)
    self.setText(initialText)
    self.setIcon(QMessageBox.Information)
    self.addButton(QMessageBox.Ok)

def showCompleted(windowTitle, initialText, parent=None):
  msgBox = CompleteDialog(windowTitle, initialText, parent)
  msgBox.show()

class ErrorBox(QMessageBox):
  def __init__(self,windowTitle, initialText, parent=None):
    super().__init__(parent)
    self.setWindowTitle(windowTitle)
    self.setText(initialText)
    self.setIcon(QMessageBox.Critical)
    self.addButton(QMessageBox.Ok)

def showError(windowTitle, initialText, parent=None):
  msgBox = ErrorBox(windowTitle, initialText, parent)
  msgBox.show()