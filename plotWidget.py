#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import numpy as np
import qdarkstyle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()
        self.initUI()
        self.data = np.arange(20).reshape([4, 5]).copy()
        self.on_draw()

    def initUI(self):
        self.fig = Figure((5.0, 4.0), dpi=50)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        # self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        #
        # self.canvas.mpl_connect('key_press_event', self.on_key_press)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        # vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)

    def on_draw(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        # self.axes.plot(self.x, self.y, 'ro')
        self.axes.imshow(self.data, interpolation='nearest')
        # self.axes.plot([1,2,3])
        self.canvas.draw()

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    form = QMainWindow()
    form.setWindowTitle("Plot Demo")
    pltWidget = PlotWidget()
    form.setCentralWidget(pltWidget)
    form.show()
    app.exec_()
