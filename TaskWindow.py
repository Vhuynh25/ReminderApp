import Classes
import time
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

        self.parent().Tasks.append(Classes.Task(text, time, item))  # append to tasks list from TaskWindow parent

        self.Text.clear()  # clear the input uis
        self.Time.clear()
        self.close()
        self.parent().show_task()


class TaskWindow(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super(TaskWindow, self).__init__(parent)
        uic.loadUi("TaskWindow.ui", self)
        self.Input = TaskInput(self)
        self.Index = 0
        self.app = app  # Task Window gets access to Qt app
        self.Tasks = None  # list of tasks imported when task window is opened
        self.alert_thread = None
        self.alerter = None

        self.List = self.TaskList

        self.Addtask.clicked.connect(self.add_task)
        self.Removetask.clicked.connect(self.remove_task)
        self.List.itemClicked.connect(self.clicked_item)
        self.Setalert.clicked.connect(self.set_alert)

    def add_task(self):
        if not self.Input.isVisible():
            self.Input.show()  # show the task input dialog and loop until it closes
            while self.Input.isVisible():
                self.app.processEvents()

    def show_task(self):
        listwid = self.List

        listwid.addItem(self.Tasks[-1].item)  # add the last task added to the task list

        self.app.processEvents()

    def clicked_item(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            item.setFlags(QtCore.Qt.ItemIsEnabled)

    def import_tasks(self, tasks):
        self.Tasks = tasks  # import list of tasks and add all of them to list wid
        for x in tasks:
            self.List.addItem(x.item)

    def remove_task(self):
        item = self.List.currentItem()
        for x in self.Tasks:
            if x.item == item:
                self.Tasks.remove(x)
        self.List.takeItem(self.List.row(item))  # remove the current task selected in list widget
        self.app.processEvents()

    def find_next_task(self):
        next_task = None
        # find incoming task in day
        for x in self.Tasks:
            if next_task is None and QtCore.QTime.currentTime().msecsSinceStartOfDay() < x.time.msecsSinceStartOfDay():
                next_task = x
            elif QtCore.QTime.currentTime().msecsSinceStartOfDay() < x.time.msecsSinceStartOfDay() < next_task.time.msecsSinceStartOfDay():
                next_task = x

        return next_task

    def alert(self):
        self.show()
        self.parent().show()

    def set_alert(self):
        alert_thread = QtCore.QThread(self)

        next_task = self.find_next_task()
        if next_task is not None:
            alerter = GenericWorker(self.alert_checker, next_task)

            alerter.moveToThread(alert_thread)

            alerter.started.connect(alerter.run)
            alerter.finished.connect(alert_thread.quit)
            alerter.finished.connect(alerter.deleteLater)
            alerter.finished.connect(self.alert)

            self.alert_thread = alert_thread
            self.alert_thread.start()
            self.alerter = alerter
            self.alerter.started.emit()
            self.hide()
            self.parent().hide()

    def alert_checker(self, current_task):
        print(current_task.text + '\n')
        while current_task is not None and current_task.time.msecsSinceStartOfDay() > QtCore.QTime.currentTime().msecsSinceStartOfDay():
            time.sleep(20)
            print(current_task.text + '\n')


class GenericWorker(QtCore.QObject):
    def __init__(self, function, *args):
        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args

    finished = QtCore.pyqtSignal()
    started = QtCore.pyqtSignal()

    #@QtCore.pyqtSlot()
    def run(self):
        # self.started.emit()
        print("checking\n")
        self.function(*self.args)
        self.finished.emit()




