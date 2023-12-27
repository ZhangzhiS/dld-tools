from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QLabel


class AvatarLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMaximumSize(100, 100)
        self.setMinimumSize(100, 100)

        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.GlobalColor.transparent)  # 填充背景为透明

    def painter_avatar(self, icon_path: str, radius: int = 10):
        p = QPixmap(icon_path).scaled(  # 加载图片并缩放和控件一样大
            100,
            100,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
