import sys
from PyQt5.QtWidgets import QScrollBar,QPushButton,QHBoxLayout, QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class ScrollBar(QWidget):
    def __init__(self):
        self.scroll = QScrollBar()
        self.scroll.setGeometry(100, 50, 200, 30)
        self.scroll.setOrientation(Qt.Horizontal)

        self.left_scroll = QPushButton('<-')


        self.right_scroll = QPushButton('->')
        #self.right_scroll.clicked.connect(self.scroll_right_action)

        self.Scroll_Lay = QHBoxLayout()
        self.Scroll_Lay.addWidget(self.left_scroll,1)
        self.Scroll_Lay.addWidget(self.scroll,8)
        self.Scroll_Lay.addWidget(self.right_scroll,1)


        super().__init__()
