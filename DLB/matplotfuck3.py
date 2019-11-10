import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import time
from threading import Thread

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(4,4)
        '''
        starter = Thread(target=self.plotter)
        starter.start()
        starter.join()
        '''

    def plotter(self):
        count = 0
        value = [0]
        bottom = range(len(value))
        while(True):
            count += 1
            value.append(count)
            bottom = range(len(value))
            time.sleep(1)

    def plot(self, x, y):
        ax = self.figure.add_subplot(111)
        ax.set_title('PyQt Matplotlib Example')
        ax.plot(x, y)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())