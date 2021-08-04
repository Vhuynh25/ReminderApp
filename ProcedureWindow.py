import sys
import Classes
import Cipher  # simple Caesar cipher
import random
import TaskWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

App = QtWidgets.QApplication(sys.argv)


class ProcedureWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ProcedureWindow, self).__init__(parent)
        uic.loadUi("ProcedureWindow.ui", self)
        self.Index = 0
        self.Procedures = []

        self.ListWid = self.ProcList

        self.AddPButton.clicked.connect(self.add_procedure)
        self.RemovePButton.clicked.connect(self.remove_procedure)
        self.EditPButton.clicked.connect(self.edit_procedure)
        self.QuitButton.clicked.connect(self.shutdown)

        self.import_procedures()

        self.TaskWindow = TaskWindow.TaskWindow(App, self)
        self.show()

    def add_procedure(self, procedure=None):
        listwid = self.ListWid
        # add new item to list widget and make it editable
        # Procedure class has access to list item
        if isinstance(procedure, str):
            item = QtWidgets.QListWidgetItem(procedure)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            listwid.addItem(item)
            self.Procedures.append(Classes.Procedure(item))

        else:
            item = QtWidgets.QListWidgetItem("New Procedure")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            listwid.addItem(item)
            self.Procedures.append(Classes.Procedure(item))

        App.processEvents()

    def edit_procedure(self):
        index = self.ListWid.currentIndex().row()
        if len(self.Procedures) > index >= 0 and not self.TaskWindow.isVisible():
            # the task window only works on one task at a time and chooses the one to work on at button press
            self.TaskWindow.import_tasks(self.Procedures[index].tasks)
            self.TaskWindow.show()

    def closeEvent(self, event):  # need
        self.export_procedures()
        self.hide()
        App.processEvents()

    def export_procedures(self):
        f = open("data.txt", "w")

        shift = random.randrange(0, 26)
        f.write(str(shift) + ':')
        for x in self.Procedures:
            # procedures are formatted like "Procedure:ProcedureName \n"
            st = 'Procedure:' + x.list_item.text() + ':\n'
            for y in x.tasks:
                # tasks are formatted like so
                # hr:minutes ap/pm | taskstring check(T/F)
                if y.item.checkState() == QtCore.Qt.Checked:
                    check = 't'
                else:
                    check = 'f'
                st += y.time.toString("h:mm ap | ") + \
                     y.text + " " + check + ' \n'
                # f.write(st)
        f.write(Cipher.encrypt(st, shift))
        f.close()

    def import_procedures(self):
        try:
            f = open("data.txt", "r")
        except:
            return
        lines = f.readlines()  # read from file

        shift = 0  # shift for the cipher
        spl = lines[0].split(':')
        if len(lines) > 0:
            shift = int(spl[0])

        for x in lines:
            # read and parse info from line
            if len(x) == 0:  # if no info is read, break for loop
                break
            else:  # else decrypt the info
                line = Cipher.encrypt(x, shift * -1)

            if "Procedure:" in line:
                current_procedure = Cipher.encrypt(spl[2], shift * -1) # used spl not line so need to decrypt it
                self.add_procedure(current_procedure)
            else:
                # tasks are formatted like so
                # hr:minutes ap/pm | taskstring check(T/F)
                spl = line.split(' ')
                t = spl[0].split(':')
                hr = int(t[0])
                minute = int(t[1])
                ampm = spl[1]
                text = spl[-3]
                check = spl[-2]
                time = QtCore.QTime(hr, minute)  # convert into QTimes
                # set up for task class
                st = time.toString("h:mm ap | ") + text
                item = QtWidgets.QListWidgetItem(st)

                if check == 't':
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Checked)  # make the task checked
                    ch = True
                else:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)  # make the task unchecked
                    ch = False

                if ampm == "PM":
                    hr += 12

                if len(self.Procedures) > 0:
                    self.Procedures[-1].tasks.append(Classes.Task(text, time, item))

        f.close()

    def remove_procedure(self):
        item = self.ListWid.currentItem()
        for x in self.Procedures:
            if x.list_item == item:
                self.Procedures.remove(x)
        self.ListWid.takeItem(self.ListWid.row(item))  # remove procedure item from list widget

        App.processEvents()

    def shutdown(self):
        self.close()
        App.quit()


# App.setQuitOnLastWindowClosed(False)

window = ProcedureWindow()

sys.exit(App.exec_())
