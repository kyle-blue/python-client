import threading
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import warnings
from matplotlib import animation
from typing import Dict
import  mplfinance as mpf

from ..Data import Data
import numpy as np

class UI(): # Thread is main thread.
    def __init__(self):

        self.fig, axes = plt.subplots()
        self.ax: plt.Axes = axes
        self.data = Data()
        # candlestick_ohlc(self.ax, [(20000, 0, 0, 0, 0)])
        # self.ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M:%S"))
        # self.lines: Dict[str, plt.Line2D] = {"bid": bid_line, "ask": ask_line}
        # self.lines["bid"].set_label("Bid")
        # self.lines["ask"].set_label("Ask")
        self.ax.set_xlabel("Date / Time")
        self.ax.set_ylabel("Price")
        self.ax.ticklabel_format(axis="y", style="plain", useOffset=False)
        # pos = self.ax.get_position()
        # self.ax.set_position([pos.x0 + 0.04, pos.y0 + 0.04,  pos.width, pos.height])
        # self.ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
        # self.ax.yaxis.set_major_locator(ticker.MaxNLocator(8))

        self.ani = self.animate()

        self.ticks = self.data.ticks
        plt.show()

    def animate(self):

        def update_bounds():
            ax = self.ax
            min1 = self.data.min1
            warnings.filterwarnings("ignore")
            x_min, x_max = np.min(min1["EURUSDp"].times), np.max(min1["EURUSDp"].times)
            x_range = x_max - x_min
            y_min, y_max = np.min(min1["EURUSDp"].bids), np.max(min1["EURUSDp"].asks)
            y_range = y_max - y_min

            old_x_lower, old_x_upper = ax.get_xbound()
            old_y_lower, old_y_upper = ax.get_ybound()
            should_update_x = x_max + (x_range / 10) > old_x_upper
            should_update_y = y_max + (y_range / 20) > old_y_upper or y_min - (y_range / 20) < old_y_lower

            if should_update_y or should_update_x:
                ax.set_xbound(x_min - (x_range / 8), x_max + (x_range / 3))
                ax.set_ybound(y_max + (y_range / 8), y_min - (y_range / 8))
                self.fig.canvas.draw()
            warnings.filterwarnings("default")


        def animate(i):  # i is call number
            mpf.plot(self.data.min1)

        # def init():
        #     candlestick_ohlc(self.ax, [(20000, 0, 0, 0, 0)])
        #     return self.ax.artists

        # mpf.make_addplot()
        return animation.FuncAnimation(self.fig, animate, interval=100, blit=False)






