from typing import Any, Optional
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QProgressBar, QSizePolicy


class QtBoxFuncProgressBar(QProgressBar):
    """
    加载动画
    """

    def __init__(self):
        super(QtBoxFuncProgressBar, self).__init__()
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(15)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.angle_inside = 0
        self.angle_outside = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateAngle)
        self.timer.start(50)  # 设置定时器间隔

    def updateAngle(self):
        self.angle_inside += 5
        self.angle_outside += 5
        self.update()

    def paintEvent(self, event: Optional[Any]):
        width = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        painter.save()
        painter.rotate(self.angle_inside)
        pen_inside = QPen()
        pen_inside.setWidthF(8.0)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen_inside.setColor(QColor("#1177b0"))
        radius_inside = int(width / 4)
        painter.setPen(pen_inside)
        painter.drawArc(
            -radius_inside,
            -radius_inside,
            radius_inside * 2,
            radius_inside * 2,
            0,
            90 * 16,
        )
        painter.drawArc(
            -radius_inside,
            -radius_inside,
            radius_inside * 2,
            radius_inside * 2,
            180 * 16,
            90 * 16,
        )

        # painter.save()
        painter.restore()
        painter.rotate(-self.angle_outside)
        pen_outside = QPen()
        pen_outside.setWidthF(8.0)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen_outside.setColor(QColor("#8abcd1"))
        radius_outside = int(width / 2 - 30)
        painter.setPen(pen_outside)
        painter.drawArc(
            -radius_outside,
            -radius_outside,
            radius_outside * 2,
            radius_outside * 2,
            90 * 16,
            90 * 16,
        )
        painter.drawArc(
            -radius_outside,
            -radius_outside,
            radius_outside * 2,
            radius_outside * 2,
            270 * 16,
            90 * 16,
        )
        painter.save()
        painter.restore()

        # 在圆环中间添加文字
        text = "请确认LOL已启动"
        font = QFont()
        font.setPixelSize(18)  # 设置字体大小#5e665b
        text_pen = QPen()
        text_pen.setColor(QColor("#5e665b"))
        painter.setPen(text_pen)
        painter.setFont(font)
        text_rect = painter.fontMetrics().boundingRect(text)

        # 计算文字的位置
        text_x = -text_rect.width() / 2
        text_y = text_rect.height() / 2
        # 绘制文字
        painter.resetTransform()  # 重置 transform，使文字不受旋转影响
        painter.translate(text_x, text_y)
        painter.drawText(
            int(self.width() / 2),
            int(self.height() / 2),
            text
        )
