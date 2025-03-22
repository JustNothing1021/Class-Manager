import random
from PySide6.QtCore    import Property, QPropertyAnimation, QCoreApplication, Qt, QRectF, QEasingCurve
from PySide6.QtGui     import QColor, QIcon, QPixmap, QMouseEvent, QPaintEvent, QPainter, QPen
from PySide6.QtCore    import QPoint, QTimer, Slot
from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect, QWidget, QMessageBox
from PySide6.QtWidgets import QListWidget, QMainWindow, QVBoxLayout, QListWidgetItem
from PySide6.QtWidgets import QMainWindow, QLabel
from typing            import Union, Tuple, Optional, Callable, List
from utils.classdtypes import Base, Thread
from utils.classdtypes import Student, Group
from utils.settings    import SettingsInfo
from utils.functions   import play_sound

class ObjectButton(QPushButton):
        "被逼出来写的学生按钮"

        def _set_color(self, col:QColor):
            """也是没办法了
            
            :param col: 要设置的颜色"""

            self.setStyleSheet("""\
    QPushButton {
        font: 8pt;
        background-color: rgba(%d, %d, %d, %d);
        border-radius: 2px;
        border: 1px solid rgb(0, 0, 0);
    }
""" % (col.red(), col.green(), col.blue(), self.opacity))
            
        @property
        def opacity(self):
            return self._opacity
        
        @opacity.setter
        def opacity(self, opacity: int):
            self._opacity = opacity
            self._set_color(self.background_color)

        

        color = Property(QColor, fset=_set_color)

        def __init__(self, 
                     text:str, 
                     parent=None, 
                     icon:Union[QIcon, QPixmap]=None, 
                     object:Union[Student, Group]=None):

            """构造函数
            
            :param icon: 图标
            :param text: 文字
            :param parent: 父窗口
            :param group: 按钮对应的对象
            """
            if icon is not None:
                super().__init__(icon=icon, text=text, parent=parent)
            else:
                super().__init__(text=text, parent=parent)
            self.object = object
            self.anim_border:QPropertyAnimation = None
            self.background_color = QColor(255, 255, 255)
            self._opacity = 162
            self.setStyleSheet(QCoreApplication.translate("Form", """\
    QPushButton {
        font: 8pt;
        background-color: rgba(255, 255, 255, %d);
        border-radius: 2px;
        border: 1px solid rgb(0, 0, 0);
    }
""" % self._opacity))


        def setOpacity(self, opacity:float):
            op = QGraphicsOpacityEffect()
            op.setOpacity(opacity)
            self.setGraphicsEffect(op)
            self.setAutoFillBackground(True)


        def flash(self, start:Tuple[int, int, int], end:Tuple[int, int, int], duration):
            """让按钮闪烁一下
            
            :param start: 起始颜色
            :param end: 结束颜色
            :param duration: 长度
            """
            self.anim = QPropertyAnimation(self, b"color")
            self.anim.setDuration(duration)
            self.anim.setStartValue(QColor(*start))
            self.anim.setEndValue(QColor(*end))
            self.anim.start()

# 1.2.12: 这一堆是我拷问半天ChatGPT写的（因为时间原因懒得研究
class ProgressAnimatedItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self._color = QColor(0, 255, 0)
        self._text = text
        self.setAutoFillBackground(True)
        self._is_selected = False  # 默认不选中
        self._hovered = False  # 是否鼠标悬浮
    
    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value

    @Property(float)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.update()  # 进度改变时，通知重绘

    def setSelected(self, selected: bool):
        """通过外部方法设置选中状态"""
        self._is_selected = selected
        self.update()  # 更新 UI

    def startProgressAnimation(self, start1, stop1, start2, stop2, duration, curve, loopCount):
        self._progress = start1
        self._color = start2
        # 创建 QPropertyAnimation 对象并绑定动画
        self._animation = QPropertyAnimation(self, b"progress")
        self._animation.setStartValue(start1)
        self._animation.setEndValue(stop1)
        self._animation.setDuration(duration)
        self._animation.setEasingCurve(curve)
        self._animation.setLoopCount(loopCount)
        if stop2:
            self._animation2 = QPropertyAnimation(self, b"color")
            self._animation2.setStartValue(start2)
            self._animation2.setEndValue(stop2)
            self._animation2.setDuration(duration)
            self._animation2.setEasingCurve(curve)
            self._animation2.setLoopCount(loopCount)
            self._animation2.start()
        self._animation.start()


    def enterEvent(self, event: QMouseEvent):
        """鼠标进入时，设置鼠标悬浮状态"""
        self._hovered = True
        self.update()  # 鼠标进入时，更新UI

    def leaveEvent(self, event: QMouseEvent):
        """鼠标离开时，恢复背景色"""
        self._hovered = False
        self.update()  # 鼠标离开时，更新UI

    def paintEvent(self, event: QPaintEvent):
        """重绘进度条和文本，支持选中状态和鼠标悬浮状态"""
        self._color = QColor(self._color.red(), self._color.green(), self._color.blue(), min(192, self._color.alpha()))
        painter = QPainter(self)
        rect = self.rect()

        # 鼠标悬浮状态：稍微改变背景色
        if self._hovered:
            painter.setBrush(QColor(235, 235, 255))  # 设置鼠标悬浮时的背景色（蓝色调）
        elif self._is_selected:
            painter.setBrush(QColor(220, 220, 255))  # 设置选中时的背景色
        else:
            painter.setBrush(QColor(255, 255, 255))  # 默认背景色
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)  # 绘制背景

        # 绘制进度条
        progress_width = rect.width() * self._progress
        fill_rect = QRectF(rect.left(), rect.top(), progress_width, rect.height())
        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(fill_rect)  # 绘制进度条

        # 绘制文字：居中显示
        painter.setPen(QPen(Qt.GlobalColor.black))  # 设置文字颜色
        text_rect = rect
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, self._text)


class ProgressAnimatedListWidgetItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.animated_item = ProgressAnimatedItem(text)

    def startProgressAnimation(self, 
                               startprogress: float, 
                               stopprogress: float, 
                               startcolor: QColor = QColor(100, 255, 100, 127), 
                               endcolor: Optional[QColor] = None,
                               duration: int = 1500, 
                               curve: QEasingCurve = QEasingCurve.Type.OutCubic, 
                               loopCount: int = 1):
        """启动进度动画
        :param start: 起始进度
        :param stop: 结束进度
        :param color: 进度条颜色
        :param duration: 动画时长
        :param curve: 动画曲线
        :param loopCount: 循环次数"""
        self.animated_item.startProgressAnimation(startprogress, stopprogress, startcolor, endcolor, duration, curve, loopCount)

    def getWidget(self):
        """返回QWidget作为item的显示内容"""
        return self.animated_item

    def setSelected(self, selected: bool):
        """同步选中状态到QWidget"""
        super().setSelected(selected)  # 调用 QListWidgetItem 的 setSelected
        self.animated_item.setSelected(selected)  # 更新自定义控件的选中状态


class QListWidget(QListWidget):
    def addItem(self, item: Union[ProgressAnimatedListWidgetItem, QListWidgetItem]):
        super().addItem(item)
        if isinstance(item, ProgressAnimatedListWidgetItem):
            widget_item = item.getWidget()
            self.setItemWidget(item, widget_item)


        
class ProgressAnimationTest(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 300)

        widget = QWidget()
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        items = ["项目 " + str(i) for i in range(1, 500 + 1)]
        self.selected_item = None  # 用来记录当前选中的 item
        for text in items:
            if random.choice([True, False]):
                item = ProgressAnimatedListWidgetItem(text)
                self.list_widget.addItem(item)
                item.startProgressAnimation(startprogress=random.randint(0, 1000) / 1000, stopprogress=random.randint(0, 1000) / 1000, startcolor=QColor(random.randint(160, 255), random.randint(160, 255), random.randint(160, 255), 127), duration=random.randint(1000, 5000), curve=QEasingCurve.Type.OutExpo, loopCount=1)

        # 双击事件
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_item_double_clicked(self, item: QListWidgetItem):
        """响应双击事件，弹出信息框"""
        # 获取点击的 item 的文本
        text = item.text()
        QMessageBox.information(self, "选中项目", f"选中{text}，索引：{self.list_widget.row(item)}")

from qfluentwidgets import InfoBar, InfoBarPosition

class SideNotice:
    "侧边栏通知，使用InfoBar实现"
    total = 0
    current = 0
    waiting:List["SideNotice"] = []
    showing:List["SideNotice"] = []
    

    def __init__(self, text:str, master:Union[QMainWindow, QWidget]=None, 
                 icon=None, sound=None, duration=5000, 
                 closeable=True, click_command:Callable=lambda: None,
                 zoom_text=True):
        """新提示的构造函数。

        :param text: 文本
        :param master: 父窗口
        :param icon: 图标
        :param sound: 声音
        :param duration: 持续时间
        :param closeable: 是否可关闭
        :param click_command: 点击命令
        """
        self.closing = False
        self.notice_text = text
        self.index = SideNotice.total
        SideNotice.total += 1
        if self not in SideNotice.waiting:
            SideNotice.waiting.append(self)
        self.master = master
        self.sound = sound
        self.icon = icon
        self.duration = duration
        self.slot = -1
        self.clicked = False
        self.closeable = closeable
        self.click_command = click_command
        self.is_showing = False
        self.is_waiting = False
        self.infobar = None

    def setSlot(self, slot: int):
        self.slot = slot

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.clicked:
            self.clicked = True
            if self.closeable:
                self.notice_close()
            self.click_command()
        return super().mousePressEvent(event)
        
    
    def show(self, slot: Optional[int] = None):
        if slot is not None:
            self.slot = slot
        self.is_waiting = True
        
        # 简化槽位分配逻辑
        if slot == -1 and hasattr(self.master, 'sidenotice_avilable_slots') and len(self.master.sidenotice_avilable_slots) > 0:
            try:
                self.slot = self.master.sidenotice_avilable_slots.pop(0)
            except:
                Base.log_exc("获取槽位失败")
        
        self.is_waiting = False
        self.is_showing = True
        
        # 记录日志
        Base.log("D", f"{self.index}号侧边提示开始展示 (文本: {repr(self.notice_text)})", "SideNotice.show")
        
        # 更新列表状态
        if self in SideNotice.waiting:
            SideNotice.waiting.remove(self) 
        if self not in SideNotice.showing:
            SideNotice.showing.append(self)
        SideNotice.current = self.index + 1
        
        # 播放声音
        if self.sound:
            Thread(target=lambda: play_sound(self.sound), daemon=True, name="SideNoticeSoundPlayer").start()
        
        # 创建并显示InfoBar
        from qfluentwidgets import InfoBarIcon
        
        # 确定InfoBar图标类型
        icon_type = InfoBarIcon.INFORMATION
        
        # 创建InfoBar
        self.infobar = InfoBar.new(
            icon=icon_type,
            title="",
            content=self.notice_text,
            orient=Qt.Orientation.Horizontal,
            isClosable=self.closeable,
            duration=self.duration,
            parent=self.master
        )
        
        # 设置位置
        # InfoBar没有setPosition方法，直接在创建时指定position参数
        # 这里不需要额外设置位置，因为已经在InfoBar.new中设置了
        
        # 如果有点击命令，连接点击事件
        if self.click_command and callable(self.click_command):
            try:
                # 尝试连接InfoBar的信号
                # 由于不确定InfoBar具体有哪些可用信号，这里使用try-except处理
                # 可能的信号包括：closeClicked, linkActivated等
                self.infobar.closeClicked.connect(self.click_command)
            except AttributeError:
                # 如果没有可用的信号，记录一个警告但不中断程序
                print(f"警告：InfoBar对象没有可用的点击信号，无法连接点击命令")
        
        # 显示InfoBar
        self.infobar.show()
        QCoreApplication.processEvents()

    @Slot()
    def notice_close(self):
        """关闭通知"""
        if self in SideNotice.showing:
            SideNotice.showing.remove(self)
        if self.closing:
            return
        self.closing = True
        
        # 如果InfoBar存在，关闭它
        if self.infobar:
            self.infobar.close()
            self.infobar = None
        
        self.is_showing = False
        
        # 释放槽位
        if hasattr(self.master, "sidenotice_avilable_slots") and self.slot != -1:
            self.master.sidenotice_avilable_slots.append(self.slot)
        
        QCoreApplication.processEvents()
    def __repr__(self):
        return f"SideNotice(text={repr(self.notice_text)}, index={self.index}, slot={self.slot})"