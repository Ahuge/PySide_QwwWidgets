from PySide import QtGui, QtCore

from task_header import TaskHeader

DURATION = 1200
UPDATE_INTERVAL = 0.0001


class Task(QtGui.QWidget):
    opened = QtCore.Signal()
    closed = QtCore.Signal()

    def __init__(self, body, parent=None):
        super(Task, self).__init__(parent)

        self.header = TaskHeader(body)
        self.body = body

        self.anim_body = None
        self.animator = QtCore.QTimeLine()
        self.animpix = QtGui.QPixmap()

        self.__max_duration = self.__base_duration = self.__duration = self.parent().DURATION
        self.__min_duration = self.__max_duration / 5
        self.__proportional_movement = self.parent().PROPORTIONAL_MOVEMENT
        self.__proportional_height = self.parent().PROPORTIONAL_HEIGHT

        self.animator.setDuration(self.__duration)
        self.animator.setUpdateInterval(self.parent().UPDATE_INTERVAL)
        self.animator.setCurveShape(QtCore.QTimeLine.EaseInOutCurve)

        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setMargin(0)

        layout.addWidget(self.header)
        layout.addWidget(self.body)
        self.body.setVisible(False)
        self.body.installEventFilter(self)

        self.header.button.toggled.connect(self.setOpen)
        self.animator.frameChanged.connect(self.animate)
        self.animator.finished.connect(self.animFinished)

    def setName(self, name):
        self.header.setTaskName(name)
        self.body.setWindowTitle(name)

    def setIcon(self, icon):
        self.header.setIcon(icon)
        self.body.setWindowIcon(icon)

    def setToggleIcon(self, icon):
        self.header.setToggleIcon(icon)

    def setOpen(self, value):
        button = self.header.toggleButton()
        if button.isChecked() == value:
            button.setChecked(value)
            arrow_type = button.arrowType()
            if arrow_type != QtCore.Qt.NoArrow:
                if value:
                    button.setArrowType(QtCore.Qt.UpArrow)
                else:
                    button.setArrowType(QtCore.Qt.DownArrow)

            if self.parent():
                _parent = self.parent().parent().parent().parent()
            else:
                _parent = None

            if _parent and not _parent.animated:
                if self.animator.state() != QtCore.QTimeLine.NotRunning:
                    if self.animator.direction == QtCore.QTimeLine.Forward:
                        self.animator.setDirection(QtCore.QTimeLine.Backward)
                    else:
                        self.animator.setDirection(QtCore.QTimeLine.Forward)
                else:
                    self.anim_body = QtGui.QWidget()
                    self.anim_body.installEventFilter(self)
                    self.anim_body.setEnabled(False)
                    self.anim_body.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

                    self.body.ensurePolished()
                    size = self.layout().closestAcceptableSize(self.body, self.body.sizeHint())
                    size = size.expandedTo(QtCore.QSize(self.width(), 0))
                    self.body.resize(size)

                    if value:
                        self.animator.setDirection(QtCore.QTimeLine.Forward)
                        self.animator.setFrameRange(0, size.height())
                        self.header.setToggleIcon(QtCore.QTimeLine.Backward)
                    else:
                        self.animator.setDirection(QtCore.QTimeLine.Backward)
                        self.animator.setFrameRange(0, self.body.height())
                        self.header.setToggleIcon(QtCore.QTimeLine.Forward)
                    if self.__proportional_movement:
                        self.update_duration()

                    if value:
                        # Switching the attribute orders so it doesnt pop.
                        self.body.setAttribute(QtCore.Qt.WA_WState_ExplicitShowHide, True)
                        self.body.setAttribute(QtCore.Qt.WA_WState_Hidden, False)
                        self.animpix = QtGui.QPixmap.grabWidget(self.body)
                        self.body.setAttribute(QtCore.Qt.WA_WState_Hidden, True)

                        self.body.hide()
                        self.layout().addWidget(self.anim_body)
                        self.anim_body.show()
                        self.animator.start()
                    else:

                        self.body.setAttribute(QtCore.Qt.WA_WState_ExplicitShowHide, True)
                        self.body.setAttribute(QtCore.Qt.WA_WState_Hidden, False)
                        self.animpix = QtGui.QPixmap.grabWidget(self.body)

                        self.layout().addWidget(self.anim_body)
                        self.anim_body.show()
                        self.body.setAttribute(QtCore.Qt.WA_WState_Hidden, True)
                        self.body.hide()
                        self.animator.start()

        else:
            if value:
                self.body.show()
            else:
                self.body.hide()

    def update_duration(self):
        widget_height = self.body.height()
        duration = int(self.__base_duration / (float(widget_height) / self.__proportional_height))
        self.__duration = max([self.__min_duration, min([self.__max_duration, duration])])
        self.animator.setDuration(self.__duration)

    def animate(self, frame):
        self.anim_body.setFixedSize(self.anim_body.width(), frame)
        self.anim_body.updateGeometry()

    def animFinished(self):
        if self.animator.currentFrame() != 0:
            self.body.show()
        self.anim_body.lower()
        self.anim_body.hide()
        self.anim_body.deleteLater()
        self.anim_body = None
        self.header.update()
        self.updateGeometry()

    def eventFilter(self, _object, event):
        if _object is self.anim_body and event.type() == QtCore.QEvent.Paint:
            painter = QtGui.QPainter(self.anim_body)
            old_rect = self.animpix.rect()
            ap_height = self.animpix.height()
            ab_height = self.anim_body.height()
            rect = old_rect.adjusted(0, ap_height-ab_height, 0, 0)
            amimbody_rect = self.anim_body.rect()
            painter.drawPixmap(amimbody_rect, self.animpix, rect)
            return True
        return False
