import random

import pyqtgraph as pg
import tushare as ts
from PyQt4 import QtCore, QtGui


# Create a subclass of GraphicsObject.
# The only required methods are paint() and boundingRect()
# (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.flagHasData = False

    def set_data(self, data):
        self.data = data  # data must have fields: time, open, close, min, max
        self.flagHasData = True
        self.generatePicture()
        self.informViewBoundsChanged()

    def generatePicture(self):
        # pre-computing a QPicture object allows paint() to run much more quickly,
        # rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        barWidth = 1 / 3.
        for (open, close, min, max, index) in self.data:
            p.drawLine(QtCore.QPointF(index, min), QtCore.QPointF(index, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(index - barWidth, open, barWidth * 2, close - open))
        p.end()

    def paint(self, p, *args):
        if self.flagHasData:
            p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        # boundingRect _must_ indicate the entire area that will be drawn on
        # or else we will get artifacts and possibly crashing.
        # (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())


class CandleWidget(pg.PlotWidget):
    def __init__(self, raw_data):
        super(CandleWidget, self).__init__()
        self.update(raw_data)
        # self.candle_data = raw_data.loc[:, ['open', 'close', 'low', 'high']]
        # r, c = self.candle_data.shape
        # self.candle_data['num'] = range(1, r + 1)
        # self.item = CandlestickItem()
        # self.item.set_data(self.candle_data.values)
        self.addItem(self.item)

    def update(self, raw_data):
        self.candle_data = raw_data.loc[:, ['open', 'close', 'low', 'high']]
        r, c = self.candle_data.shape
        self.candle_data['num'] = range(1, r + 1)
        self.item = CandlestickItem()
        self.item.set_data(self.candle_data.values)


# app = QtGui.QApplication([])
# df = ts.get_hist_data('000681', '2015-01-01', ktype='w')
# r, c = df.shape
# print(r)
# cData = df.copy().loc[:, ['open', 'close', 'low', 'high']]
# cData['num'] = range(1, r + 1)
#
# print(cData)
# # cData = np.array(cData)
# item = CandlestickItem()
# item.set_data(cData.values)
#
# plt = pg.plot()
# plt.addItem(item)
# plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
#
#
# def update():
#     global item
#     df = ts.get_hist_data('000681', '2015-01-01', ktype='d')
#     r, c = df.shape
#     print(r)
#     cData = df.loc[:, ['open', 'close', 'low', 'high']]
#     cData['num'] = range(1, r + 1)
#     item.set_data(cData.values)
#     # app.processEvents()  ## force complete redraw for every plot
#
#
# timer = QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(10000)

# df = ts.get_hist_data('000681', '2015-01-01', ktype='w')
# print(enumerate(df))
# for (value) in df.head(10).values:
#     print(value)
# print(type(value))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
