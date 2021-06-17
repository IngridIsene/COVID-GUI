import pickle
from functools import partial
import math
import Classes
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollBar, QLabel, QInputDialog, QMenuBar
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Classes.menuBar import MenuBar
from Classes.scrollBar import ScrollBar
from Classes.plotClass import plotClass
from Classes.plotClassFull import plotClassFull
from Classes.HideClass import HideClass
from functions import epi_dict, episodes, GET_DF_FOR_DATE, get_ColorDict, plot_settings, patient_settings
from pandas import DataFrame
import pandas as pd
from pathlib import Path
import os
import matplotlib
from os import path


# PATHS
MAIN_PATH = str(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute()) # /Users/user/PyCharm_Projects
EXCEL_PATH = MAIN_PATH+'/EXCEL'
GUI_PATH = MAIN_PATH+'/GUI'
PICKLE_PATH = GUI_PATH+'/PICKLE'
DATA_PATH = MAIN_PATH+'/DATA'


class Plot_window(QWidget):
    def __init__(self, ID, DATE):
        super().__init__()
        objects             = pickle.load(open(PICKLE_PATH+'/pickle.pkl', "rb"))
        self.DICT_ID_df     = objects[1]
        self.ID             = ID
        self.DATE           = DATE
        self.count          = 0

        with open(PICKLE_PATH+'/plot_settings.pkl', "rb") as f:
            plot_s = pickle.load(f)

        with open(PICKLE_PATH+'/patient_settings.pkl', "rb") as s:
            patient_s = pickle.load(s)


        if bool(plot_s) == False:
            self.first_plot_setting()
            self.new_date_setting()
        else:
            self.stored_config(plot_s)

            if self.ID in patient_s.keys():
                if self.DATE in patient_s[self.ID]:
                    self.stored_date_setting(patient_s[self.ID][self.DATE])
                else:
                    self.new_date_setting()

            else:
                self.new_date_setting()

        self.setup()
        self.setLayout(self.mainLayout)
        self.showFullScreen()

    def first_plot_setting(self):
        self.interval               = 30
        self.current_full           = 'heart_rate_min'
        self.hidePlot               = HideClass(False, False, [], [])  # SET TO FALSE WHEN PLOT CLASS HIDE IS FIXED
        self.hiddenPlots            = []
        self.hideLine               = HideClass(True, False, [], [])
        self.hiddenLines            = []
        self.Vline_win              = HideClass(False, True, [], [])
        self.checked_vline_ax       = []
        self.hiddenVline_ax         = []
        self.Vlines                 = {}
        self.PrevIntervals          = []
        self.PrevInterval_Objects   = {}

    def stored_config(self, plot_s):
        self.interval               = plot_s['interval']
        self.current_full           = plot_s['current_full']
        self.hidePlot               = HideClass(False, False, plot_s['hidePlot'],[])
        self.hiddenPlots            = plot_s['hiddenPlots']
        self.hideLine               = HideClass(True, False, plot_s['hideLine'],[])
        self.hiddenLines            = plot_s['hiddenLines']
        self.Vline_win              = HideClass(False, True, [],plot_s['Vline_win'])
        self.checked_vline_ax       = plot_s['checked_vline_ax']
        self.hiddenVline_ax         = plot_s['hiddenVline_ax']
        self.Vlines                 = plot_s['Vlines']
        self.PrevIntervals          = plot_s['PrevIntervals']
        self.PrevInterval_Objects   = plot_s['PrevInterval_Objects']


    def new_date_setting(self):
        self.start_tick             = 0
        self.SLEEP                  = plotClass(False, None, None)
        self.HR                     = plotClass(False, None, None)
        self.RESP                   = plotClass(False, None, None)
        self.HRV                    = plotClass(False, None, None)
        self.REL                    = plotClass(False, None, None)
        self.FULL                   = plotClassFull()
        self.df, self.markerList    = GET_DF_FOR_DATE(self.ID, self.DATE, self.DICT_ID_df)
        self.x_list                 = range(len(self.df['time']))
        self.points                 = {}
        self.texts                  = {}
        self.MarkedIntervals        = []
        self.pickle_state           = False



    def stored_date_setting(self, patient_s):
        self.start_tick             = patient_s['start_tick']
        self.SLEEP                  = plotClass(False, None, None)
        self.HR                     = plotClass(True, patient_s['HR']['fig'], patient_s['HR']['axes'])
        self.RESP                   = plotClass(True, patient_s['RESP']['fig'], patient_s['RESP']['axes'])
        self.HRV                    = plotClass(True, patient_s['HRV']['fig'], patient_s['HRV']['axes'])
        self.REL                    = plotClass(True, patient_s['REL']['fig'], patient_s['REL']['axes'])
        self.FULL                   = plotClassFull()
        self.df                     = patient_s['df']
        self.markerList             = patient_s['markerList']
        self.x_list                 = patient_s['x_list']
        self.points                 = patient_s['points']
        self.texts                  = patient_s['texts']
        self.MarkedIntervals        = patient_s['MarkedIntervals']
        self.pickle_state           = True


    def setup(self):
        self.set_Layout()

        for w in self.hidePlot.get_selected_items():
            self.get_widget(w).set_tick_params(False)
        self.get_widget(self.hidePlot.get_selected_items()[len(self.hidePlot.get_selected_items())-1]).set_tick_params(True)

        self.connect_menuBar()
        self.plotData()

        self.SLEEP.set_sleep_legend()
        self.SLEEP.fig.subplots_adjust(top = 0.48,bottom = 0.055,left = 0.03,right = 0.98,hspace = 0.303,wspace = 0.205)
        self.adjust_all()

        self.SLEEP.set_yaxis_visible(False)
        self.SLEEP.set_xaxis_visible(False)

        self.setInterval()
        self.set_y_ticks()
        self.set_legend()

        self.draw_FULL()
        self.hidePlot_submit()
        self.hideLine_submit()
        self.hideVlines_submit()




    def __getstate__(self):
        plot_s      = self.__dict__.copy()
        patient_s   = self.__dict__.copy()


        for key in plot_s.copy():
            if key not in plot_settings:
                plot_s.pop(key)

        plot_s['hidePlot']  = self.hidePlot.get_unselected_items()
        plot_s['hideLine']  = self.hideLine.get_unselected_items()
        plot_s['Vline_win'] = self.Vline_win.get_selected_items()


        for key in patient_s.copy():
            if key not in patient_settings:
                patient_s.pop(key)

        patient_s['SLEEP']  = patient_s['SLEEP'].__getstate__()
        patient_s['HR']     = patient_s['HR'].__getstate__()
        patient_s['RESP']   = patient_s['RESP'].__getstate__()
        patient_s['REL']    = patient_s['REL'].__getstate__()
        patient_s['HRV']    = patient_s['HRV'].__getstate__()
        patient_s['FULL']   = patient_s['FULL'].__getstate__()

        return plot_s, patient_s


    def set_Layout(self):
        self.connect_menuBar()
        self.scrollBar = ScrollBar()
        self.scrollBar.scroll.setMaximum(len(self.x_list) - self.interval)
        self.scrollBar.scroll.valueChanged.connect(self.scroll_action)
        self.scrollBar.scroll.setValue(self.start_tick)
        self.scrollBar.left_scroll.clicked.connect(self.scroll_left_action)
        self.scrollBar.right_scroll.clicked.connect(self.scroll_right_action)



        toolbar = NavigationToolbar(self.HR, self)

        Label = QVBoxLayout()
        Label.addWidget(toolbar)
        Label.addWidget(QLabel('Patient ID: ' + str(self.ID)))
        Label.addWidget(QLabel('Date: ' + str(self.DATE)))

        SLEEP = QVBoxLayout()
        SLEEP.addWidget(self.SLEEP, 1)


        self.HR_Widget = QWidget()
        lay1 = QVBoxLayout()
        lay1.addWidget(self.HR)
        lay1.setSpacing(0)
        lay1.setContentsMargins(0,0,0,0)
        self.HR_Widget.setLayout(lay1)

        self.RESP_Widget = QWidget()
        lay2 = QVBoxLayout()
        lay2.addWidget(self.RESP)
        lay2.setSpacing(0)
        lay2.setContentsMargins(0, 0, 0, 0)
        self.RESP_Widget.setLayout(lay2)

        self.HRV_Widget = QWidget()
        lay3 = QVBoxLayout()
        lay3.addWidget(self.HRV)
        lay3.setSpacing(0)
        lay3.setContentsMargins(0, 0, 0, 0)
        self.HRV_Widget.setLayout(lay3)

        self.REL_Widget = QWidget()
        lay4 = QVBoxLayout()
        lay4.addWidget(self.REL)
        lay4.setSpacing(0)
        lay4.setContentsMargins(0, 0, 0, 0)
        self.REL_Widget.setLayout(lay4)

        EKG = QVBoxLayout()
        EKG.addWidget(self.HR_Widget)
        EKG.addWidget(self.RESP_Widget)
        EKG.addWidget(self.HRV_Widget)
        EKG.addWidget(self.REL_Widget)
        EKG.setSpacing(0)
        EKG.setContentsMargins(0,0,0,0)




        FULL = QVBoxLayout()
        FULL.addWidget(self.FULL)

        PlotLay = QVBoxLayout()
        PlotLay.addLayout(SLEEP, 1)
        PlotLay.addLayout(EKG, 8)
        PlotLay.addLayout(FULL, 1)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.menuBar)
        self.mainLayout.addLayout(Label, 0.5)
        self.mainLayout.addLayout(PlotLay, 8)
        self.mainLayout.addLayout(self.scrollBar.Scroll_Lay, 1)



    def draw_FULL(self):
        self.FULL.full_epi_ax.cla()
        self.FULL.plotFULL(self.current_full, self.df, self.markerList)
        self.FULL.set_yticks(self.get_widget_of_full())
        self.FULL.set_x_lim(0, len(self.x_list) - 1)
        self.updateColorPatch()
        self.FULL.fig.canvas.draw()


    def get_widget_of_full(self):
        for k,v in epi_dict.items():
            for v in epi_dict[k]:
                if v == self.current_full:
                    y = self.get_widget(k).axes.get_yticks()
                    break
        return y

    def get_widget_of_subheader(self,sub):
        for k,v in epi_dict.items():
            for v in epi_dict[k]:
                if v == sub:
                    ax = self.get_widget(k)
                    break
        return ax


    def set_y_ticks(self):
        self.HR.set_yticks(0, 150, 20)
        self.RESP.set_yticks(0, 30, 5)
        self.HRV.set_yticks(0, 400, 50)
        self.REL.set_yticks(0, 10000, 2000)

    def adjust_all(self):
        for i in self.get_all_main_wigets():
            i.fig.subplots_adjust(top=0.848,bottom=0.177,left=0.031,right=0.983,hspace=0.2,wspace=0.2)

    def set_legend(self):
        for i in self.get_all_main_wigets():
            i.set_legend()


    def setInterval(self):
        for i in self.get_all_wigets():
            i.axes.set_xlim(self.start_tick,self.start_tick+self.interval)

    def plotData(self):
        if self.pickle_state == False:
            for i in epi_dict.keys():
                ax = self.get_widget(i).axes
                ax.set_title(i, loc='left', fontsize=7)

                for episode in epi_dict[i]:
                    if 'min' in episode:
                        string = 'min'
                        color = '#1f77b4'


                    elif 'median' in episode:
                        string = 'median'
                        color = '#ff7f0e'

                    elif 'max' in episode:
                        string = 'max'
                        color = '#2ca02c'

                    ax.plot(self.df['time'], self.df[episode], linestyle='-', color=color, label=string)

                    if len(self.markerList) != 0:
                        for m in self.markerList:
                            ax.plot(m, self.df[episode].loc[self.df['time']==m], linestyle='-', marker='.', color=color, label='_'+string)


        self.plotSleep()




    def plotSleep(self):
        index = 0
        ColorDict = get_ColorDict()

        for sleepstatus in self.df['sleep_status'].values:
            color = ColorDict[str(sleepstatus)]
            self.SLEEP.axes.axvspan(self.x_list[index], self.x_list[index + 1], color=color)
            self.FULL.get_ax('sleep').axvspan(self.x_list[index], self.x_list[index + 1], color=color)

            index += 1
            if index == len(self.x_list) - 1:
                break



    def connect_menuBar(self):
        self.menuBar = QMenuBar()

        # MENU HEADERS
        HideMenu = self.menuBar.addMenu(' Show/Hide')
        PlotMenu = self.menuBar.addMenu(' Change Full Episode')
        DateMenu = self.menuBar.addMenu(' Change Date')
        IntervalMenu = self.menuBar.addMenu(' Set Interval')
        PatientMenu = self.menuBar.addMenu(' Change PatientID')

        GridMenu = self.menuBar.addMenu(' Grid')
        grid = GridMenu.addMenu('Grid')
        vertical = GridMenu.addMenu('Vertical Line')
        horizontal = GridMenu.addMenu('Horizontal Line')

        AddMarker = self.menuBar.addMenu(' Add Marker')
        dot = AddMarker.addMenu('Dot')
        triangle = AddMarker.addMenu('Triangle')
        vline = AddMarker.addMenu('Vertical Line')
        hline = AddMarker.addMenu('Horizontal Line')
        ex = AddMarker.addMenu('X')
        point = AddMarker.addMenu('Point')

        AddText = self.menuBar.addMenu(' Add Text')

        colorText = AddText.addMenu('Colored Text')

        HideMenu.addAction('Show/Hide Plots', self.hidePlot_show)
        HideMenu.addAction('Show/Hide Lines', self.hideLine_show)
        HideMenu.addAction('Show/Hide V-lines', self.hideVlines_show)
        for epi in episodes:
            PlotMenu.addAction(epi, self.change_plot)
        for date in self.DICT_ID_df[self.ID]['date'].unique():
            DateMenu.addAction(date, self.change_date)


        IntervalMenu.addAction('X-Interval', self.set_x_interval)
        IntervalMenu.addAction('Y-Interval: Heart Rate', partial(self.set_y_interval, 'Heart Rate'))
        IntervalMenu.addAction('Y-Interval: Respiration Rate',partial(self.set_y_interval, 'Respiration Rate'))
        IntervalMenu.addAction('Y-Interval: Heart Rate Variability',partial(self.set_y_interval, 'Heart Rate Variability'))
        IntervalMenu.addAction('Y-Interval: Relative Stroke Volume',partial(self.set_y_interval, 'Relative Stroke Volume'))
        IntervalMenu.addAction('Default Y-Intervals', self.set_y_ticks)

        grid.addAction('Grid ON', partial(self.grids, 'g', True))
        grid.addAction('Grid OFF', partial(self.grids, 'g', False))
        vertical.addAction('Vertical ON', partial(self.grids, 'v', True))
        vertical.addAction('Vertical OFF', partial(self.grids, 'v', False))
        horizontal.addAction('Horizontal ON', partial(self.grids, 'h', True))
        horizontal.addAction('Horizontal OFF', partial(self.grids, 'h', False))

        PatientMenu.addAction('Change PatientID', self.new_patient)

        dot.addAction('Green', partial(self.activate,'o','green'))
        dot.addAction('Red',partial(self.activate,'o','red'))
        dot.addAction('Blue', partial(self.activate,'o','blue'))
        triangle.addAction('Green', partial(self.activate, '^', 'green'))
        triangle.addAction('Red', partial(self.activate, '^', 'red'))
        triangle.addAction('Blue', partial(self.activate, '^', 'blue'))
        vline.addAction('Green', partial(self.activate, '|', 'green'))
        vline.addAction('Red', partial(self.activate, '|', 'red'))
        vline.addAction('Blue', partial(self.activate, '|', 'blue'))
        hline.addAction('Green', partial(self.activate, '_', 'green'))
        hline.addAction('Red', partial(self.activate, '_', 'red'))
        hline.addAction('Blue', partial(self.activate, '_', 'blue'))
        ex.addAction('Green', partial(self.activate, 'x', 'green'))
        ex.addAction('Red', partial(self.activate, 'x', 'red'))
        ex.addAction('Blue', partial(self.activate, 'x', 'blue'))
        point.addAction('Green', partial(self.activate, '.', 'green'))
        point.addAction('Red', partial(self.activate, '.', 'red'))
        point.addAction('Blue', partial(self.activate, '.', 'blue'))
        AddMarker.addAction('Delete', self.activate_Delete)

        AddText.addAction('Plain Text',partial(self.activate_Text,'p'))
        colorText.addAction('Green', partial(self.activate_Text, 'c'))
        colorText.addAction('Red', partial(self.activate_Text, 'c'))
        colorText.addAction('Blue', partial(self.activate_Text, 'c'))
        AddText.addAction('Delete Text', self.activate_DeleteText)

        Extract = self.menuBar.addMenu(' Extract Data')
        Extract.addAction('Set Interval', partial(self.activate_MarkInterval,True,None))
        self.prev = Extract.addMenu('Previous Intervals ')

        for p in self.PrevIntervals:
            self.prev.addAction(p, partial(self.activate_MarkInterval,False,p))

        Extract.addAction('Import to Excel', self.create_Excel)
        Extract.addAction('Delete Interval', self.deleteInterval)





    def scroll_action(self):
        self.start_tick = self.scrollBar.scroll.value()
        self.setInterval()
        self.updateColorPatch()
        self.redrawAll()

    def scroll_right_action(self):
        self.start_tick = self.start_tick + self.interval
        self.scrollBar.scroll.setValue(self.start_tick)
        self.setInterval()
        self.updateColorPatch()
        self.redrawAll()

    def scroll_left_action(self):
        self.start_tick = self.start_tick - self.interval
        self.scrollBar.scroll.setValue(self.start_tick)
        self.setInterval()
        self.updateColorPatch()
        self.redrawAll()

    def updateColorPatch(self):
        self.FULL.delete_patches()
        self.FULL.draw_patch(self.start_tick, self.interval)




    def get_widget(self, header):
        if header == 'Heart Rate':
            return self.HR
        elif header == 'Respiration Rate':
            return self.RESP
        elif header == 'Heart Rate Variability':
            return self.HRV
        elif header == 'Relative Stroke Volume':
            return self.REL

    def get_outer_widget(self,header):
        if header == 'Heart Rate':
            return self.HR_Widget
        elif header == 'Respiration Rate':
            return self.RESP_Widget
        elif header == 'Heart Rate Variability':
            return self.HRV_Widget
        elif header == 'Relative Stroke Volume':
            return self.REL_Widget



    def redrawAll(self):
        for i in self.get_all_wigets():
            i.fig.canvas.draw()

    def get_all_wigets(self):
        return [self.SLEEP,self.HR, self.RESP, self.HRV, self.REL]

    def get_all_main_wigets(self):
        return [self.HR, self.RESP, self.HRV, self.REL]

    def get_all_axes(self):
        return [self.HR.axes, self.RESP.axes, self.HRV.axes, self.REL.axes]

    def get_ax(self,header):
        if header == 'Heart Rate':
            return self.HR.axes
        elif header == 'Respiration Rate':
            return self.RESP.axes
        elif header == 'Heart Rate Variability':
            return self.HRV.axes
        elif header == 'Relative Stroke Volume':
            return self.REL.axes

    # MENUBAR #######################################################################################################

    @QtCore.pyqtSlot()
    def hideLine_show(self):
        self.hideLine.show()
        self.hideLine.button.clicked.connect(self.hideLine_submit)

    def hideLine_submit(self):
        showList = self.hideLine.get_selected_items()

        hideList = self.hideLine.get_unselected_items()


        for subheader in hideList:
            if subheader in episodes:
                self.hiddenLines.append(subheader)
                for header in epi_dict.keys():
                    if subheader in epi_dict[header]:
                        ax = self.get_widget(header)

                        for line in ax.axes.get_lines():
                            if '_' in line.get_label():
                                string = line.get_label().split('_')[1]


                                if string in subheader:
                                    line.set_visible(False)

                            elif line.get_label() in subheader:
                                line.set_visible(False)

                        ax.fig.canvas.draw()

        for showsubheader in showList:
            if showsubheader in episodes:
                if showsubheader in self.hiddenLines:
                    self.hiddenLines.remove(showsubheader)

                    for header in epi_dict.keys():
                        if showsubheader in epi_dict[header]:
                            ax = self.get_widget(header)

                            for line in ax.axes.get_lines():
                                if line.get_label() in showsubheader:
                                    line.set_visible(True)
                            ax.fig.canvas.draw()

        self.hideLine.close()

    @QtCore.pyqtSlot()
    def hidePlot_show(self):
        self.hidePlot.show()
        self.hidePlot.button.clicked.connect(self.hidePlot_submit)


    def hidePlot_submit(self):
        showList = self.hidePlot.get_selected_items()
        hideList = self.hidePlot.get_unselected_items()

        for i in hideList:
            self.hiddenPlots.append(i)
            widget = self.get_outer_widget(i)
            widget.setHidden(True)


        for i in showList:
            if i in self.hiddenPlots:
                self.hiddenPlots.remove(i)
                widget = self.get_outer_widget(i)
                widget.setHidden(False)


        for w in self.hidePlot.get_selected_items():
            self.get_widget(w).set_tick_params(False)
        self.get_widget(self.hidePlot.get_selected_items()[len(self.hidePlot.get_selected_items())-1]).set_tick_params(True)

        self.hidePlot.close()


    @QtCore.pyqtSlot()
    def hideVlines_show(self):
        self.Vline_win.show()
        self.Vline_win.button.clicked.connect(self.hideVlines_submit)

    def hideVlines_submit(self):

        for header in self.Vline_win.get_selected_items():
            ax = self.get_widget(header).axes

            if ax in self.checked_vline_ax:
                pass
            else:
                self.checked_vline_ax.append(ax)
                if ax in self.hiddenVline_ax:
                    for line in self.Vlines[ax]:
                        line.set_visible(True)
                    self.hiddenVline_ax.remove(ax)

                else:
                    self.Vlines[ax] = []
                    for x, min, max in zip(self.x_list, self.df[epi_dict[header][0]],
                                           self.df[epi_dict[header][2]]):
                        line = ax.vlines(x, min, max, color='black', linestyles='solid')
                        self.Vlines[ax].append(line)

        for header in self.Vline_win.get_unselected_items():
            ax = self.get_widget(header).axes

            if ax in self.checked_vline_ax:
                for line in self.Vlines[ax]:
                    line.set_visible(False)
                self.checked_vline_ax.remove(ax)

        self.redrawAll()
        self.Vline_win.close()


    @QtCore.pyqtSlot()
    def change_plot(self):
        action = self.sender()
        self.current_full = action.text()
        self.draw_FULL()

    @QtCore.pyqtSlot()
    def set_x_interval(self):
        text, ok = QInputDialog.getText(self, 'Interval Settings', 'Set x-interval:')
        if ok:
            self.interval = int(text)
            self.setInterval()
            self.updateColorPatch()
            self.redrawAll()

    @QtCore.pyqtSlot()
    def set_y_interval(self, header):
        widget = self.get_widget(header)

        text, ok = QInputDialog.getText(self, 'Interval Settings', 'Set y-interval:\n (from,to,interval): ex. 0,100,20')
        if ok:
            string = text.split(',')
            fra = int(string[0])
            til = int(string[1])
            inter = int(string[2])
            ticks = range(fra, til + inter, inter)
            widget.axes.set_yticks(ticks)
            widget.axes.set_ylim(fra, til)
            widget.fig.canvas.draw()

    @QtCore.pyqtSlot()
    def grids(self, line, bool):
        for widget in self.get_all_main_wigets():
            ax = widget.axes

            if line == 'g':
                ax.grid(bool)
            elif line == 'h':
                ax.yaxis.grid(bool)
            elif line == 'v':
                ax.xaxis.grid(bool)

        self.redrawAll()

    @QtCore.pyqtSlot()
    def change_date(self):
        self.SAVE()
        action = self.sender()
        self.DATE = action.text()
        self.plotWin = Plot_window(self.ID, self.DATE)
        self.plotWin.showFullScreen()
        self.close()

    @QtCore.pyqtSlot()
    def new_patient(self):
        self.SAVE()
        self.first_win = Classes.choice_window.Choice_window()
        self.first_win.showFullScreen()
        self.close()

    @QtCore.pyqtSlot()
    def activate_MarkInterval(self, bool, prev):
        if bool == True:
            text, ok = QInputDialog.getText(self, 'INTERVAL', 'ENTER NAME FOR INTERVAL:')
            if ok:
                self.cid = {}
                for i in self.get_all_main_wigets():
                    cid = i.fig.canvas.mpl_connect('button_press_event', partial(self.MarkInterval,text))
                    self.cid[i] = cid
        else:
            self.cid = {}
            for i in self.get_all_main_wigets():
                cid = i.fig.canvas.mpl_connect('button_press_event', partial(self.MarkInterval, prev))
                self.cid[i] = cid



    def MarkInterval(self,text,event):
        if self.count == 0:
            ax = event.inaxes
            self.p1 = ax.plot(event.xdata, event.ydata, marker='.', color='purple',ms=10, ls="", label='_'+text)
            self.a1 = ax.annotate(text+' START', xy=(event.xdata - 0.3, event.ydata + 0.1),weight='bold')
            self.start_time = self.df['time'].loc[round(event.xdata)]
            self.redrawAll()
            self.count+=1


        else:
            ax = event.inaxes
            self.p2 = ax.plot(event.xdata, event.ydata, marker='.', color='purple', ms=10, ls="", label='_'+text)
            self.a2 = ax.annotate(text + ' END', xy=(event.xdata - 0.3, event.ydata + 0.5),weight='bold')
            self.end_time = self.df['time'].loc[round(event.xdata)]

            self.MarkedIntervals.append([text, self.start_time,self.end_time])

            if text not in self.PrevIntervals:
                self.PrevIntervals.append(text)
                self.prev.addAction(text, partial(self.activate_MarkInterval, False, text))


            self.PrevInterval_Objects[text] = [ax,self.p1,self.a1,self.p2,self.a2]
            self.redrawAll()

            for i in self.get_all_main_wigets():
                i.fig.canvas.mpl_disconnect(self.cid[i])
            self.cid = {}

            self.count = 0
            self.start_time = None
            self.end_time = None

        self.create_Excel()


    def deleteInterval(self):
        text, ok = QInputDialog.getText(self, 'DELETE INTERVAL', 'ENTER NAME TO REMOVE INTERVAL :')
        if ok:
            if text in self.PrevInterval_Objects.keys():
                ax_name = self.PrevInterval_Objects[text][0].get_title(loc='left')
                ax = self.get_ax(ax_name)

                for key in self.PrevInterval_Objects.keys():
                    for i in self.PrevInterval_Objects[key][1:]:

                        if isinstance(i, matplotlib.text.Annotation):
                            for element in ax.texts:
                                if element.get_text() == i.get_text():
                                    element.remove()

                        else:
                            for element in ax.get_lines():
                                if element.get_label() == '_'+key:
                                    element.remove()


                self.redrawAll()

                for element in self.MarkedIntervals:
                    if text in element:
                        self.MarkedIntervals.remove(element)

                self.create_Excel()





    @QtCore.pyqtSlot()
    def create_Excel(self):
        ID_path = EXCEL_PATH+'/'+str(self.ID)
        if path.exists(ID_path) == False:
            os.mkdir(ID_path)
        Date_path = ID_path+'/'+str(self.DATE)+'.xlsx'

        writer = pd.ExcelWriter(Date_path, engine='xlsxwriter')
        df = DataFrame(self.MarkedIntervals, columns=['INTERVAL', 'START TIME', 'END TIME'])
        df.to_excel(writer, sheet_name='Intervals')

        for interval in self.MarkedIntervals:
            name = interval[0]
            start_t = interval[1]
            end_t = interval[2]

            index_start = self.df[self.df['time']==start_t].index[0]
            end_start = self.df[self.df['time'] == end_t].index[0]

            interval_df = self.df[index_start:end_start+1]
            interval_df.drop('ans',inplace=True, axis=1)
            interval_df.drop('delta', inplace=True, axis=1)
            interval_df.to_excel(writer, sheet_name=name)

        writer.save()



    @QtCore.pyqtSlot()
    def activate(self,markerstyle,color):
        self.MarkerStyle = markerstyle
        self.MarkerColor = color

        self.cid = {}
        for i in self.get_all_main_wigets():
            cid = i.fig.canvas.mpl_connect('button_press_event', self.marker_onclick)
            self.cid[i]=cid


    def marker_onclick(self, event):
        ax = event.inaxes
        point = ax.plot(event.xdata, event.ydata, marker=self.MarkerStyle, color=self.MarkerColor, ms=10, ls="", label=str(event.xdata))
        if ax not in self.points.keys():
            self.points[ax] = {}

        if event.xdata not in self.points[ax].keys():
            self.points[ax][event.xdata] = []

        self.points[ax][event.xdata].append(point)
        self.redrawAll()

        for i in self.get_all_main_wigets():
            i.fig.canvas.mpl_disconnect(self.cid[i])

        self.cid = {}


    @QtCore.pyqtSlot()
    def activate_Delete(self):
        self.cid = {}
        for i in self.get_all_main_wigets():
            cid = i.fig.canvas.mpl_connect('button_press_event', self.deletePoint)
            self.cid[i] = cid

    def deletePoint(self, event):
        ax = event.inaxes

        for key in self.points.keys():
            if key.get_title(loc='left') == ax.get_title(loc='left'):
                x = key
                self.points[self.get_ax(x.get_title(loc='left'))] = self.points.pop(x)
                break


        ax_dict = self.points.get(ax)
        absolute_difference_function = lambda list_value: abs(list_value - event.xdata)
        closest_x_value = min(ax_dict.keys(), key=absolute_difference_function)


        if event.xdata >= math.floor(closest_x_value) and event.xdata <= math.ceil(closest_x_value):

            punkter = self.points[ax][closest_x_value]
            if len(punkter) > 1:
                y_list = []
                for punkt in punkter:
                    y_list.append(punkt[0].get_data()[1])

                absolute_difference_function = lambda list_value: abs(list_value - event.ydata)
                closest_y_value = min(y_list, key=absolute_difference_function)

                for element in ax.get_lines():
                    label = element.get_label()
                    if '_' in label:
                        s = label.split('_')
                        if s[1] == self.points[ax][closest_x_value][y_list.index(closest_y_value)][0].get_label():
                            element.remove()

                self.points[ax][closest_x_value][y_list.index(closest_y_value)][0].remove()
                self.points[ax][closest_x_value].remove(y_list.index(closest_y_value))


            else:

                for element in ax.get_lines():
                    label = element.get_label()
                    if '_' in label:
                        s = label.split('_')
                        if s[1] == self.points[ax][closest_x_value][0][0].get_label():
                            element.remove()

                self.points[ax][closest_x_value][0][0].remove()
                del self.points[ax][closest_x_value]


            self.redrawAll()
            for i in self.get_all_main_wigets():
                i.fig.canvas.mpl_disconnect(self.cid[i])
            self.cid = {}

    @QtCore.pyqtSlot()
    def activate_Text(self, type):
        color = self.sender().text()

        self.cid = {}
        for i in self.get_all_main_wigets():
            cid = i.fig.canvas.mpl_connect('button_press_event', partial(self.text_onclick, type, color))
            self.cid[i] = cid

    def text_onclick(self,type,color,event):
        text, ok = QInputDialog.getText(self, 'ADD TEXT', 'Write text here:')
        if ok:
            ax = event.inaxes
            if type == 'box':
                txt = ax.text(event.xdata, event.ydata, text, bbox={'facecolor': color, 'alpha': 0.5, 'pad': 10})
            elif type == 'p':
                txt = ax.text(event.xdata, event.ydata, text)
            elif type == 'c':
                txt = ax.text(event.xdata, event.ydata, text, color=color)


            if ax not in self.texts.keys():
                self.texts[ax] = {}

            if event.xdata not in self.texts[ax].keys():
                self.texts[ax][event.xdata] = []

            self.texts[ax][event.xdata].append(txt)

            self.redrawAll()

            for i in self.get_all_main_wigets():
                i.fig.canvas.mpl_disconnect(self.cid[i])
            self.cid = {}




    def activate_DeleteText(self):
        self.cid = {}
        for i in self.get_all_main_wigets():
            cid = i.fig.canvas.mpl_connect('button_press_event', self.deleteText)
            self.cid[i] = cid

    def deleteText(self,event):
        ax = event.inaxes

        for key in self.texts.keys():
            if key.get_title(loc='left') == ax.get_title(loc='left'):
                x = key
                self.texts[self.get_ax(x.get_title(loc='left'))] = self.texts.pop(x)
                break


        ax_dict = self.texts.get(ax)
        absolute_difference_function = lambda list_value: abs(list_value - event.xdata)
        closest_x_value = min(ax_dict.keys(), key=absolute_difference_function)

        if event.xdata >= math.floor(closest_x_value) - 1 and event.xdata <= math.ceil(closest_x_value) + 1:
            tekster = self.texts[ax][closest_x_value]
            if len(tekster) > 1:
                y_list = []
                for tekst in tekster:
                    y_list.append(tekst[0].get_position()[1])

                absolute_difference_function = lambda list_value: abs(list_value - event.ydata)
                closest_y_value = min(y_list, key=absolute_difference_function)
                for element in ax.texts:
                    if element.get_text() == self.texts[ax][closest_x_value][y_list.index(closest_y_value)].get_text():
                        x = element
                        self.texts[ax][closest_x_value][y_list.index(closest_y_value)] = x
                        break

                ax.texts.remove(self.texts[ax][closest_x_value][y_list.index(closest_y_value)])
                self.texts[ax][closest_x_value].remove(y_list.index(closest_y_value))

            else:
                for element in ax.texts:
                    if element.get_text() == self.texts[ax][closest_x_value][0].get_text():
                        x = element
                        self.texts[ax][closest_x_value][0] = x
                        break

                ax.texts.remove(self.texts[ax][closest_x_value][0])
                del self.texts[ax][closest_x_value]


            self.redrawAll()
            for i in self.get_all_main_wigets():
                i.fig.canvas.mpl_disconnect(self.cid[i])
            self.cid = {}

    def SAVE(self):
        plot_settings, patient_settings = self.__getstate__()
        #print(plot_settings['hidePlot'])

        with open(PICKLE_PATH+'/plot_settings.pkl', "wb") as f:
            pickle.dump(plot_settings, f)

        with open(PICKLE_PATH+'/patient_settings.pkl', "rb") as f:
            patient_s = pickle.load(f)

        if self.ID not in patient_s.keys():
            patient_s[self.ID] = {}
        patient_s[self.ID][self.DATE] = patient_settings

        with open(PICKLE_PATH+'/patient_settings.pkl', "wb") as f:
            pickle.dump(patient_s, f)

    def closeEvent(self, event):
        self.SAVE()





