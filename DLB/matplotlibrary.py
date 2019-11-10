import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random
from threading import Thread
import time

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        grid1 = plt.grid(True)   # линии вспомогательной сетки

        plt.show()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        #self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.button = QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.button)
        self.setLayout(layout)
        starter = Thread(target=self.plot)
        starter.start()
        starter.join()

    def plot(self, data):
        ''' Here I want to refresh the Plot every 6 sec '''
        left_border = 0.0
        old_border = 0.0
        while(True):
            # instead of ax.hold(False)
            self.figure.clear()

            plt.plot([left_border, left_border + 1.0], [old_border, old_border + 1.0])
            left_border += 1.0
            old_border += 1.0
            print('Plot: ', len(graph1), graph1)

            # create an axis
            #ax = self.figure.add_subplot(111)

            # discards the old graph
            # ax.hold(False) # deprecated, see above

            # plot data
            #ax.plot(data, '*-')

            # refresh canvas
            #self.canvas.draw()
            time.sleep(6)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())