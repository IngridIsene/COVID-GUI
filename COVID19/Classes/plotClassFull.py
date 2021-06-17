import sys
from PyQt5.QtWidgets import QApplication
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
import numpy as np
import pickle
from functions import get_ColorDict

class plotClassFull(FigureCanvasQTAgg):
    def __init__(self):

        self.fig = Figure(figsize=(15, 7.5))
        super(plotClassFull, self).__init__(self.fig)

        self.spec5 = self.fig.add_gridspec(ncols=1, nrows=2, width_ratios=[15], height_ratios=[0.5,2])
        self.full_sleep_ax = self.fig.add_subplot(self.spec5[0, 0])
        self.full_epi_ax = self.fig.add_subplot(self.spec5[1, 0])

        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.035, bottom=0.010, right=0.985, top=0.95, hspace=0.303, wspace=0.205)

        self.set_axis_visible()

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes = {'fig':attributes['fig'],'full_sleep_ax':attributes['full_sleep_ax'], 'full_epi_ax': attributes['full_epi_ax']}
        return attributes

    def get_ax(self,head):
        if head == 'sleep':
            return self.full_sleep_ax
        if head == 'epi':
            return self.full_epi_ax

    def plotFULL(self, episode, df, markerList):
        self.full_epi_ax.plot(df['time'], df[episode], linestyle='-', color='red')

        if len(markerList) != 0:
            for m in markerList:
                self.full_epi_ax.plot(m, df[episode].loc[df['time'] == m], linestyle='-', marker='.', color='red')


    def set_axis_visible(self):
        self.full_sleep_ax.xaxis.set_visible(False)
        self.full_sleep_ax.yaxis.set_visible(False)
        self.full_epi_ax.xaxis.set_visible(False)
        self.full_epi_ax.yaxis.set_visible(False)

    def set_x_lim(self, start, stop):
        self.full_sleep_ax.set_xlim(start, stop)
        self.full_epi_ax.set_xlim(start, stop)


    def draw_patch(self,start_tick,interval):
        y_ticks = self.full_epi_ax.get_yticks()
        left, bottom, width, height = (start_tick, y_ticks[0], interval, max(y_ticks))
        rect = plt.Rectangle((left, bottom), width, height, color="red", alpha=0.1)
        self.full_epi_ax.add_patch(rect)
        self.fig.canvas.draw()

    def delete_patches(self):
        if len(self.full_epi_ax.patches) > 0:
            for p in self.full_epi_ax.patches:
                p.remove()



    def set_yticks(self,y):
        self.full_epi_ax.set_yticks(range(y[0], y[len(y) - 1] + (y[1] - y[0]), (y[1] - y[0])))


