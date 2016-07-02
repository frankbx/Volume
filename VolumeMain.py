import sys

import psutil
import qdarkstyle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from volumeWidgets import KWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)
        logDockWidget = QDockWidget('log', self)
        logDockWidget.setObjectName('LogDockWidget')
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Volume")
        self.initMenu()
        self.initStatusBar()

    def initMenu(self):
        menubar = self.menuBar()
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.openAbout)
        sysMenu = menubar.addMenu('System')

        sysMenu.addAction(exitAction)
        functionMenu = menubar.addMenu('Function')

        # 帮助
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction(aboutAction)

    def initStatusBar(self):
        self.statusLabel = QLabel()
        self.statusLabel.setAlignment(Qt.AlignLeft)
        status = self.statusBar()
        status.addPermanentWidget(self.statusLabel)
        self.statusLabel.setText(self.getCpuMemory())
        status.showMessage('Ready', 5000)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateStatusBar)
        self.timer.start(1000)

    def updateStatusBar(self):
        self.statusLabel.setText(self.getCpuMemory())

    def getCpuMemory(self):
        cpuPercent = psutil.cpu_percent()
        memoryPercent = psutil.virtual_memory().percent
        return 'CPU使用率：%d%%   内存使用率：%d%%' % (cpuPercent, memoryPercent)

    def openAbout(self):
        aboutWidget = AboutWidget(self)
        aboutWidget.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
                                     'Are you sure to exit?', QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class AboutWidget(QDialog):
    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle('About Volume')

        text = u"""
            Developed by traders, for traders.

            License：MIT
            """

        label = QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    sys.exit(app.exec_())
