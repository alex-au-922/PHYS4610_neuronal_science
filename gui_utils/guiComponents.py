from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class QHSeperationLine(QFrame):
  def __init__(self):
    super().__init__()
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
    return

class QVSeperationLine(QFrame):
  def __init__(self):
    super().__init__()
    self.setFixedWidth(20)
    self.setFrameShape(QFrame.VLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    return