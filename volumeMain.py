import sys

import psutil
import qdarkstyle
import tushare as ts
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import dataAcquisition
from volumeWidgets import CandleWidget


class MainWindow(QMainWindow):
    def __init__(self, raw_data):
        super(MainWindow, self).__init__()

        self.candleWidget = CandleWidget(raw_data)

        self.setCentralWidget(self.candleWidget)
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
        sysMenu = menubar.addMenu('System')
        sysMenu.addAction(exitAction)

        functionMenu = menubar.addMenu('Function')
        # updateAction = QAction('Update', self)
        # updateAction.triggered().connect(self.updateCandle)
        # functionMenu.addAction(updateAction)

        # 帮助
        helpMenu = menubar.addMenu('Help')
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.openAbout)
        helpMenu.addAction(aboutAction)

    def updateCandle(self):
        df = ts.get_hist_data('000681', '2015-01-01', ktype='d')
        self.candleWidget.update(df)

    def initStatusBar(self):
        self.statusLabel = QLabel()
        self.statusLabel.setAlignment(Qt.AlignLeft)
        status = self.statusBar()
        status.addPermanentWidget(self.statusLabel)
        self.statusLabel.setText(self.getCpuMemory())
        status.showMessage('Ready', 5000)
        self.statusTimer = QTimer()
        self.statusTimer.timeout.connect(self.updateStatusBar)
        self.statusTimer.start(1000)

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
    df = dataAcquisition.get_sh_data()
    mainWindow = MainWindow(df)
    mainWindow.showMaximized()
    sys.exit(app.exec_())
