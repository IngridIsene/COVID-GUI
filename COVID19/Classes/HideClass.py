
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.Qt import Qt
from functions import epi_dict


class HideClass(QWidget):
    def __init__(self,child_status,uncheck_status,unselectedList, selectedList):
        super().__init__()
        layout = QVBoxLayout()
        self.child_status = child_status
        self.uncheck_status = uncheck_status

        self.tree = QTreeWidget()
        for header in epi_dict.keys():
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, header)

            if self.uncheck_status == False:
                parent.setCheckState(0, Qt.Checked)
            if self.uncheck_status == True:
                parent.setCheckState(0, Qt.Unchecked)

            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            if self.child_status == True:
                for x in epi_dict[header]:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setText(0, x)
                    child.setCheckState(0, Qt.Checked)



        self.handle_Unselected(unselectedList)
        self.handle_Selected(selectedList)


        self.button = QPushButton('Submit')

        layout.addWidget(self.tree)
        layout.addWidget(self.button)
        self.setLayout(layout)


    def handle_Selected(self,selectedList):
        for item in selectedList:
            if self.child_status == True:
                if item not in epi_dict.keys():
                    self.tree.findItems(str(item), Qt.MatchExactly | Qt.MatchRecursive)[0].setCheckState(0, Qt.Checked)

            if self.child_status == False:
                self.tree.findItems(str(item), Qt.MatchExactly | Qt.MatchRecursive)[0].setCheckState(0, Qt.Checked)




    def handle_Unselected(self,unselectedList):
        for item in unselectedList:
            if self.child_status == True:
                if item not in epi_dict.keys():
                    self.tree.findItems(str(item), Qt.MatchExactly | Qt.MatchRecursive)[0].setCheckState(0, Qt.Unchecked)

            if self.child_status == False:
                self.tree.findItems(str(item), Qt.MatchExactly | Qt.MatchRecursive)[0].setCheckState(0, Qt.Unchecked)


    def get_unselected_items(self):
        unchecked_items = []
        def recurse(parent_item):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                grand_children = child.childCount()
                if grand_children > 0:
                    recurse(child)
                if child.checkState(0) != Qt.Checked:
                    unchecked_items.append(child.text(0))


        recurse(self.tree.invisibleRootItem())
        return unchecked_items


    def get_selected_items(self):
        checked_items = []
        def recurse(parent_item):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                grand_children = child.childCount()
                if grand_children > 0:
                    recurse(child)
                if child.checkState(0) == Qt.Checked:
                    checked_items.append(child.text(0))

        recurse(self.tree.invisibleRootItem())
        return checked_items
