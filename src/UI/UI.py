import threading
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import warnings
from matplotlib import animation
from typing import Dict

from ..Data import Data
import numpy as np

class UI(): # Thread is main thread.
    def __init__(self):

        self.fig, axes = plt.subplots()
        self.ax: plt.Axes = axes
        bid_line, ask_line, = self.ax.plot(np.array([]), np.array([]), '-g', [], [], '-r')
        self.ax.xaxis_date()
        self.lines: Dict[str, plt.Line2D] = {"bid": bid_line, "ask": ask_line}
        self.lines["bid"].set_label("Bid")
        self.lines["bid"].set_label("Ask")

        self.data = Data()
        self.ani = self.animate()
        plt.show()

    def animate(self):

        def update_bounds():
            ax = self.ax
            ticks = self.data.ticks
            warnings.filterwarnings("ignore")
            x_min, x_max = np.min(ticks["EURUSDp"]["times"]), np.max(ticks["EURUSDp"]["times"])
            x_range = x_max - x_min
            y_min, y_max = np.min(ticks["EURUSDp"]["bids"]), np.max(ticks["EURUSDp"]["asks"])
            y_range = y_max - y_min

            old_x_lower, old_x_upper = ax.get_xbound()
            old_y_lower, old_y_upper = ax.get_ybound()
            should_update_x = x_max > old_x_upper
            should_update_y = y_max > old_y_upper or y_min < old_y_lower

            if should_update_y or should_update_x:
                ax.set_xbound(x_min - (x_range / 8), x_max + (x_range / 3))
                ax.set_ybound(y_max + (y_range / 8), y_min - (y_range / 8))
                self.fig.canvas.draw()
            warnings.filterwarnings("default")


        def animate(i):  # i is call number
            ticks = self.data.ticks
            lines = self.lines
            if "EURUSDp" not in ticks:
                return lines["bid"], lines["ask"],
            update_bounds()
            lines["bid"].set_data(ticks["EURUSDp"]["times"], ticks["EURUSDp"]["bids"])
            lines["ask"].set_data(ticks["EURUSDp"]["times"], ticks["EURUSDp"]["asks"])

            return lines["bid"], lines["ask"],

        def init():
            ticks = self.data.ticks
            lines = self.lines
            if "EURUSDp" not in ticks:
                return lines["bid"], lines["ask"],
            update_bounds()
            lines["bid"].set_data(np.array([]), np.array([]))
            lines["ask"].set_data(np.array([]), np.array([]))

            return self.ax.get_lines()

        return animation.FuncAnimation(self.fig, animate, init_func=init, interval=100, blit=True)






