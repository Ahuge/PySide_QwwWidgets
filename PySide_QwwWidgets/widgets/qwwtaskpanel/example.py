from PySide import QtGui, QtCore
from task_panel import QwwTaskPanel


def main():
    app = QtGui.QApplication([])
    panel = QwwTaskPanel()

    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QPushButton("Stuff"))
    layout.addWidget(QtGui.QLineEdit("Words"))
    big = QtGui.QPushButton("Big")
    big.setMinimumHeight(240)
    layout.addWidget(big)
    layout.addWidget(QtGui.QLineEdit("Words"))
    widget.setLayout(layout)
    widget.setMinimumHeight(500)
    widget.setStyleSheet("QWidget {border: 2px dotted red}")
    icon = QtGui.QIcon(r"..\..\images\fileopen.png")
    panel.addTask(widget, icon=icon, label="Open")

    button = QtGui.QPushButton("Do")
    icon = QtGui.QIcon(r"..\..\images\filesave.png")
    panel.addTask(button, icon=icon, label="Save")

    button = QtGui.QPushButton("Do")
    icon = QtGui.QIcon(r"..\..\images\twocolor.png")
    panel.addTask(button, icon=icon, label="Colour")

    panel.show()
    app.exec_()


if __name__ == "__main__":
    main()
