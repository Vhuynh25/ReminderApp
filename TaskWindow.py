import Classes
import Cipher
import random
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic


class TaskInput(QtWidgets.QDialog):  # dialog to make a new task
    def __init__(self, parent=None):
        super(TaskInput, self).__init__(parent)
        uic.loadUi("TaskInput.ui", self)
        self.Ok.clicked.connect(self.get_input)
        self.Cancel.clicked.connect(self.close)

    def get_input(self):
        text = self.Text.toPlainText()
        time = self.Time.time()

        st = time.toString("h:mm ap | ") + text

        item = QtWidgets.QListWidgetItem(st)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)

        self.parent().tasks.append(Classes.Task(text, time, item))  # append to tasks list from TaskWindow parent

        self.Text.clear()  # clear the input uis
        self.Time.clear()
        self.close()
        self.parent().show_task()


class TaskWindow(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super(TaskWindow, self).__init__(parent)
        uic.loadUi("Main.ui", self)
        self.Input = TaskInput(self)
        self.Index = 0
        self.app = app  # Task Window gets access to Qt app
        self.tasks = None  # list of tasks imported when task window is opened

        self.List = QtWidgets.QListWidget(self)
        self.List.setGeometry(10, 60, 301, 291)

        self.Addtask.clicked.connect(self.add_task)
        self.Removetask.clicked.connect(self.remove_task)
        self.List.itemClicked.connect(self.clicked_item)

    def add_task(self):
        if not self.Input.isVisible():
            self.Input.show()  # show the task input dialog and loop until it closes
            while self.Input.isVisible():
                self.app.processEvents()

    def show_task(self):
        listwid = self.List

        listwid.addItem(self.tasks[-1].item)  # add the last task added to the task list

        self.app.processEvents()

    def clicked_item(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            item.setFlags(QtCore.Qt.ItemIsEnabled)

    def import_tasks(self, tasks):
        self.tasks = tasks  # import list of tasks and add all of them to list wid
        for x in tasks:
            self.List.addItem(x.item)

    def remove_task(self):
        item = self.List.currentItem()

        self.List.takeItem(self.List.row(item))  # remove the current task selected in list widget
        self.app.processEvents()