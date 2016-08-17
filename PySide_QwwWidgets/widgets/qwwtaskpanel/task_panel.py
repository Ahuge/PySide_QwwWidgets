from PySide import QtGui, QtCore

from task import Task


class QwwTaskPanel(QtGui.QWidget):
    DURATION = 1200
    UPDATE_INTERVAL = 0.0001
    PROPORTIONAL_MOVEMENT = True
    PROPORTIONAL_HEIGHT = 10
    currentIndexChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(QwwTaskPanel, self).__init__(parent)

        self.tasks = []
        self.panel = None
        self.toggle_icon = QtGui.QIcon(r"..\..\images\arrow-down.png")
        self.current = None
        self.animated = False

        scroll_area = QtGui.QScrollArea()
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setMargin(0)
        layout.addWidget(scroll_area)

        self.panel = QtGui.QWidget(scroll_area.viewport())
        self.panel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.MinimumExpanding)
        self.panel.setObjectName("ww_taskpanel_panel")

        panel_layout = QtGui.QVBoxLayout(self.panel)
        panel_layout.addStretch()
        scroll_area.setWidget(self.panel)
        scroll_area.setWidgetResizable(True)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)

    def addTask(self, task_widget, icon=None, label=None):
        self.insertTask(self.taskCount(), task_widget, icon, label)

    def insertTask(self, index, task_widget, icon=None, label=None):
        if icon is None:
            icon = QtGui.QIcon()
        if task_widget is None:
            return

        task = Task(task_widget, parent=self)
        task.setToggleIcon(self.toggle_icon)
        if label is None:
            task.setName(task.windowTitle())
        else:
            task.setName(label)
            task.setWindowTitle(label)

        if icon is None:
            task.setIcon(task.windowIcon())
        else:
            task.setIcon(icon)
            task.setWindowIcon(icon)

        self.panel.layout().insertWidget(index, task)
        self.tasks.insert(index, task)

        if len(self.tasks) == 1:
            self.setCurrentIndex(0)
            task.header.button.setChecked(True)
        task.show()

    def removeTask(self, index):
        if index < 0 or index > self.taskCount():
            return
        task = self.tasks.pop(index)
        if self.taskCount() <= index:
            self.setCurrentIndex(self.taskCount()-1)
        body = task.body
        body.setParent(self)
        del task

    def currentTask(self):
        if self.current and 0 < self.current < self.taskCount():
            return self.tasks[self.current]
        return None

    def task(self, index):
        if index < 0 or index > self.taskCount():
            return None
        task = self.tasks[index]
        if task:
            return task.body
        return None

    def taskCount(self):
        return len(self.tasks)

    def indexOf(self, task):
        if task in self.tasks:
            return self.tasks.index(task)
        return None

    def setToggleIcon(self, icon):
        self.toggle_icon = icon
        for task in self.tasks:
            task.setToggleIcon(icon)

    def setTaskIcon(self, index, icon):
        if index < 0 or index > self.taskCount():
            return
        task = self.tasks[index]
        if task:
            task.setIcon(icon)

    def setTaskTitle(self, index, title):
        if index < 0 or index > self.taskCount():
            return
        task = self.tasks[index]
        if task:
            task.setName(title)

    def setTaskName(self, index, name):
        if index < 0 or index > self.taskCount():
            return
        task = self.tasks[index]
        if task:
            task.body.setObjectName(name)

    def setCurrentIndex(self, index):
        if index < 0 or index > self.taskCount() or index == self.current:
            return
        if self.current:
            task = self.tasks[self.current]
            task.setOpen(False)
        self.current = index
        task = self.tasks[self.current]
        task.setOpen(True)
        self.currentIndexChanged.emit(index)
