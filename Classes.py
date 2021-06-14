

class Task:
    def __init__(self, text, t, listitem):
        self.text = text  # string of task
        self.time = t  # QTime

        self.item = listitem  # item for QT list widget


class Procedure:
    def __init__(self, item):
        self.list_item = item  # item for QT list widget

        self.tasks = []  # list of tasks

    def append_task(self, task):
        self.tasks.append(task)

    def set_tasks(self, tasks):
        self.tasks = tasks

    def remove_task(self, s):
        for x in self.tasks:
            if s == x.text:
                self.tasks.remove(x)
