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

class plotClass(FigureCanvasQTAgg):
    def __init__(self, pickle_state,fig, ax):
        if pickle_state == True:
            self.fig = fig
            self.axes = ax
            self.hide_point_labels()
            super(plotClass, self).__init__(self.fig)
            self.fig.tight_layout()
        else:
            self.fig = Figure(figsize=(15, 7.5))
            self.axes = self.fig.add_subplot(111)
            super(plotClass, self).__init__(self.fig)
            self.fig.tight_layout()




    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes = {'fig':attributes['fig'],'axes':attributes['axes']}
        return attributes


    def set_legend(self):
        self.axes.legend(loc='upper right', ncol=3, prop={'size': 7})

    def set_title(self, title):
        self.axes.set_title(title, loc='left', fontsize=7)

    def set_xaxis_visible(self, bool):
        self.axes.xaxis.set_visible(bool)

    def set_yaxis_visible(self, bool):
        self.axes.yaxis.set_visible(bool)

    def set_tick_params(self, bool):
        self.axes.tick_params(labelbottom=bool)

    def set_yticks(self,fra,to,interval):
        self.axes.set_yticks(range(fra, to, interval))

    def get_current_yticks(self):
        self.axes.get_yticks()

    def set_sleep_legend(self):
        # legend for sleepstatus
        custom_lines = []
        states = []
        for k, v in get_ColorDict().items():
            custom_lines.append(Line2D([0], [0], color=v, lw=4))
            states.append(k)
        self.axes.legend(custom_lines, states, loc='lower left', bbox_to_anchor=(0, 1, 1, 0), ncol=6, mode='expand')

    def adjust(self):
        self.fig.subplots_adjust(top=0.848, bottom=0.177, left=0.031, right=0.983, hspace=0.2, wspace=0.2)

    def hide_point_labels(self):
        for element in self.axes.get_lines():
            label = element.get_label()
            if self.num_there(label) == True:
                element.set_label('_'+ str(label))

    def num_there(self,s):
        return any(i.isdigit() for i in s)
