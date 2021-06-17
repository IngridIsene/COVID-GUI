from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QWidget



class MenuBar(QWidget):
    def __init__(self):
        self.mainMenu = QMenuBar()

        # MENU HEADERS
        self.HideMenu       = self.mainMenu.addMenu(' Show/Hide')
        self.PlotMenu       = self.mainMenu.addMenu(' Change Full Episode')
        self.DateMenu       = self.mainMenu.addMenu(' Change Date')
        self.IntervalMenu   = self.mainMenu.addMenu(' Set Interval')
        self.PatientMenu    = self.mainMenu.addMenu(' Change PatientID')

        self.GridMenu       = self.mainMenu.addMenu(' Grid')
        self.grid           = self.GridMenu.addMenu('Grid')
        self.vertical       = self.GridMenu.addMenu('Vertical Line')
        self.horizontal      = self.GridMenu.addMenu('Horizontal Line')

        self.AddMarker      = self.mainMenu.addMenu(' Add Marker')
        self.dot            = self.AddMarker.addMenu('Dot')
        self.triangle       = self.AddMarker.addMenu('Triangle')
        self.vline          = self.AddMarker.addMenu('Vertical Line')
        self.hline          = self.AddMarker.addMenu('Horizontal Line')
        self.ex             = self.AddMarker.addMenu('X')
        self.point          = self.AddMarker.addMenu('Point')

        self.AddText        = self.mainMenu.addMenu(' Add Text')
        self.PreviousTexts  = self.AddText.addMenu('Previous Texts')
        self.colorText      = self.AddText.addMenu('Colored Text')




        super().__init__()
