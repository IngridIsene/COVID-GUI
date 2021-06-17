import sys
from PyQt5.QtWidgets import QApplication,  QWidget, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Classes.plot_window import Plot_window
import pickle
import os
from pathlib import Path

# PATHS
MAIN_PATH = str(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute()) # /Users/user/PyCharm_Projects
EXCEL_PATH = MAIN_PATH+'/EXCEL'
GUI_PATH = MAIN_PATH+'/GUI'
PICKLE_PATH = GUI_PATH+'/PICKLE'
DATA_PATH = MAIN_PATH+'/DATA'

class Choice_window(QWidget):

    def __init__(self):
        objects = pickle.load(open(PICKLE_PATH+"/pickle.pkl", "rb"))
        self.DICT_ID_df = objects[1]

        super().__init__()
        self.model = QStandardItemModel()

        self.comboID = QComboBox()
        self.comboID.setModel(self.model)

        self.comboDate = QComboBox()
        self.comboDate.setModel(self.model)

        self.submit = QPushButton('SUBMIT')
        self.submit.clicked.connect(self.open_plot)

        #ADD VALUES TO COMBOBOX
        ID_Date = {}
        ID_Date['PATIENT ID'] = ['DATE']
        for id, df in self.DICT_ID_df.items():
            ID_Date[id] = df['date'].unique()

        for k,v in ID_Date.items():
            ID = QStandardItem(k)
            self.model.appendRow(ID)
            for value in v:
                date = QStandardItem(value)
                ID.appendRow(date)
        self.comboID.currentIndexChanged.connect(self.updateIDCombo)
        self.updateIDCombo(0)

        #LAYOUT
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.comboID)
        mainLayout.addWidget(self.comboDate)
        mainLayout.addWidget(self.submit)
        self.setLayout(mainLayout)
        self.showFullScreen()



    def updateIDCombo(self, index):
        indx = self.model.index(index, 0, self.comboID.rootModelIndex())
        self.comboDate.setRootModelIndex(indx)
        self.comboDate.setCurrentIndex(0)

    def open_plot(self):
        ID = self.comboID.currentText()
        DATE = self.comboDate.currentText()
        self.plotWin = Plot_window(ID,DATE)
        self.plotWin.showFullScreen()
        self.close()





