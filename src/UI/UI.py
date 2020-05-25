import threading
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation

from ..Data import Data

class UI(): # Thread is main thread.
    def __init__(self):

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], '-g')
        self.data = Data()
        self.ani = self.animate()

        plt.show()

    def animate(self):
        def animate(i):
            ticks = self.data.ticks
            line = self.line
            ax = self.ax
            if "EURUSDp" not in ticks:
                return line
            ax.clear()
            ax.plot_date(ticks["EURUSDp"]["times"], ticks["EURUSDp"]["bids"], '-g')
            ax.plot_date(ticks["EURUSDp"]["times"], ticks["EURUSDp"]["asks"], '-r')
            # line.set_xdata(ticks["EURUSDp"]["times"])
            # line.set_ydata(ticks["EURUSDp"]["bids"])

            return line

        return animation.FuncAnimation(self.fig, animate, interval=100)



    def init(self):
        pass


