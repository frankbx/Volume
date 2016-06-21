import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.image = QImage()
        self.dirty = False
        self, filename = None
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)
        logDockWidget = QDockWidget('log', self)
        logDockWidget.setObjectName('LogDockWidget')
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)
        self.printer = None
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage('Ready', 5000)
