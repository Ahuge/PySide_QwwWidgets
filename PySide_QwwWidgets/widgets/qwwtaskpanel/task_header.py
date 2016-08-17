from PySide import QtCore, QtGui


class TaskHeader(QtGui.QFrame):
    BACKWARDS_ICON_PATH = r"..\..\images\arrow-up.png"
    FORWARDS_ICON_PATH = r"..\..\images\arrow-down.png"

    def __init__(self, widget, parent=None):
        super(TaskHeader, self).__init__(parent)
        self.widget = widget
        self.icon = None
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameRect(QtCore.QRect().adjusted(0, 8, 0, 0))
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        # layout.setMargin(1)
        self.spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        layout.addItem(self.spacer)

        self.text = QtGui.QLabel()
        font = self.text.font()
        font.setBold(True)
        self.text.setFont(font)

        self.button = QtGui.QToolButton()
        self.button.setObjectName("__qt__passive_button")
        self.button.setAutoRaise(True)
        self.button.setCheckable(True)
        self.button.setArrowType(QtCore.Qt.DownArrow)

        layout.addWidget(self.text)
        layout.addWidget(self.button)

    def setToggleIcon(self, icon):
        if icon == QtCore.QTimeLine.Backward:
            self.button.setIcon(QtGui.QIcon(self.BACKWARDS_ICON_PATH))
            return
        elif icon == QtCore.QTimeLine.Forward:
            self.button.setIcon(QtGui.QIcon(self.FORWARDS_ICON_PATH))
            return
        if icon is None:
            icon = QtGui.QIcon()
        self.button.setIcon(icon)
        if icon is None:
            self.button.setArrowType(QtCore.Qt.UpArrow if self.button.isChecked() else QtCore.Qt.DownArrow)
        else:
            self.button.setArrowType(QtCore.Qt.NoArrow)

    def setTaskName(self, name):
        self.text.setText(name)
        self.layout().invalidate()
        self.update()

    def setIcon(self, icon):
        self.icon = icon
        if icon is None:
            self.spacer.changeSize(0, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        else:
            self.spacer.changeSize(50, 16, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.spacer.invalidate()
        self.layout().invalidate()
        self.update()

    def paintEvent(self, event):
        super(TaskHeader, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        ico = QtGui.QIcon.Disabled
        if self.isEnabled():
            ico = QtGui.QIcon.Active
        state = QtGui.QIcon.Off
        if self.toggleButton().isChecked():
            state = QtGui.QIcon.On
        self.icon.paint(painter, QtCore.QRect(2, 1, 32, 32), QtCore.Qt.AlignCenter, ico, state)

    def toggleButton(self):
        return self.button
