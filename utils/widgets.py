import random
from PySide6.QtCore    import Property, QPropertyAnimation, QCoreApplication, Qt, QRectF, QEasingCurve
from PySide6.QtGui     import QColor, QIcon, QPixmap, QMouseEvent, QPaintEvent, QPainter, QPen
from PySide6.QtCore    import QPoint, QTimer, Slot
from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect, QWidget, QMessageBox
from PySide6.QtWidgets import QListWidget, QMainWindow, QVBoxLayout, QListWidgetItem
from PySide6.QtWidgets import QMainWindow, QLabel
from utils.base        import Student, Group
from typing            import Union, Tuple, Optional, Callable, List
from utils.base        import Base, Thread
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


class SideNotice(QWidget):
    "侧边栏通知"
    total = 0
    current = 0
    waiting:List["SideNotice"] = []
    in_curve = QEasingCurve.Type.OutCubic
    out_curve = QEasingCurve.Type.InQuad
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
        super().__init__(master)
        self.closing = False
        self.notice_text = text
        self.index = SideNotice.total
        SideNotice.total += 1
        if self not in SideNotice.waiting:
            SideNotice.waiting.append(self)
        self.label = QLabel(self)
        self.setStyleSheet(QCoreApplication.translate("Form", "background-color: rgb(255, 255, 255); font: 8pt; border: 1px solid rgb(0, 0, 0);") + (
            f"background-image: url({icon});  background-position: center; background-repeat: no-repeat;" if icon is not None else ""
        ))
        self.label.setStyleSheet(QCoreApplication.translate("Form", "background-color: rgb(255, 255, 255); font: 8pt;  border: 1px solid rgb(0, 0, 0);"))
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.setParent(master)
        self.master = master
        self.sound = sound
        self.icon = icon
        self.duration = duration
        self.slot = -1
        self.clicked = False
        self.setFixedWidth(min(160 + max((len(text) - 10) * 8, 0), 240))
        self.setFixedHeight(40)
        self.label.setFixedWidth(min(160 + max((len(text) - 10) * 8, 0), 240))
        self.label.setFixedHeight(40)
        self.closeable = closeable
        self.click_command = click_command
        self.is_showing = False
        self.is_waiting = False
        if len(text) > 40 and zoom_text: # 如果文本过长就缩小字体
            self.label.setStyleSheet(QCoreApplication.translate("Form", "background-color: rgb(255, 255, 255); font: 7pt; border: 1px solid rgb(0, 0, 0);"))
        self.move(self.master.geometry().width(), 40)
        super().show()

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
        if slot == -1:
            try:
                while self.master.is_running: # 等到主窗口有多余的槽位显示
                    try:
                        # minimized = self.master.isMinimized()
                        # visible = self.master.isVisible()
                        # first = SideNotice.current == self.index

                        if len(self.master.sidenotice_avilable_slots):
                            # Base.log("D", f"{self.index}尝试获取槽位", "SideNotice.show")
                            self.slot = self.master.sidenotice_avilable_slots.pop(0)
                        # else:
                        #     if SideNotice.waiting != [] and not SideNotice.waiting[0].showing and all([SideNotice.waiting[0].index <= n.index for n in SideNotice.waiting]) and len(self.master.sidenotice_avilable_slots):
                        #         SideNotice.waiting[0].show()
                            
                        QCoreApplication.processEvents()
                    except:
                        pass
                    if self.slot != -1:
                        # Base.log("D", F"{self.index}号提示分配到槽位：{self.slot}", "SideNotice.show")
                        break
            except:
                Base.log_exc("显示提示失败")
        
        self.is_waiting = False
        self.is_showing = True
        duration = 600 / SettingsInfo.current.animation_speed
        Base.log("D", f"{self.index}号 (位于槽位{self.slot}) 侧边提示开始展示 (文本: {repr(self.notice_text)})", "SideNotice.show")
        if self in SideNotice.waiting:
            SideNotice.waiting.remove(self) 
        if self not in SideNotice.showing:
            SideNotice.showing.append(self)
        SideNotice.current = self.index + 1
        self.startpoint = QPoint(self.master.geometry().width() + 20, self.slot * 40)
        self.endpoint = QPoint(self.master.geometry().width() - self.width(), self.slot * 40)
        self.timer = QTimer()
        if self.sound:
            Thread(target=lambda: play_sound(self.sound), daemon=True, name="SideNoticeSoundPlayer").start()
        self.showanimation = QPropertyAnimation(self, b"pos")
        self.showanimation.setStartValue(self.startpoint)
        self.showanimation.setEndValue(self.endpoint)
        self.showanimation.setEasingCurve(self.in_curve)
        self.showanimation.setDuration(duration)
        self.showanimation.start()
        self.timer.start(duration + self.duration)
        self.timer.timeout.connect(self.notice_close)
        QCoreApplication.processEvents()

    @Slot()
    def notice_close(self):
        if self in SideNotice.showing:
            SideNotice.showing.remove(self)
        if self.closing:
            return
        self.closing = True
        self.timer.stop()
        duration = 800 / SettingsInfo.current.animation_speed
        self.closeanimation = QPropertyAnimation(self, b"pos")
        self.closeanimation.setStartValue(self.endpoint)
        self.closeanimation.setEndValue(self.startpoint)
        self.closeanimation.setEasingCurve(self.out_curve)
        self.closeanimation.setDuration(duration)
        self.closeanimation.start()
        self.timer2 = QTimer()
        self.timer2.start(duration + 5)
        self.timer2.timeout.connect(self.notice_exit)
        QCoreApplication.processEvents()

    @Slot()
    def notice_exit(self):
        self.master.sidenotice_avilable_slots.append(self.slot)
        self.timer2.stop()
        Base.log("D", f"位于槽位{self.slot}的侧边提示结束展示 (文本: {repr(self.notice_text)})", "SideNotice.show")
        # if SideNotice.waiting:
            # Base.log("D", f"当前等待队列：{[t.index for t in SideNotice.waiting]}, 当前空位：{self.master.sidenotice_avilable_slots}", "SideNotice.show")
        self.master.sidenotice_avilable_slots.sort()
        self.hide()
        self.destroy()
    def __repr__(self):
        return f"SideNotice(text={repr(self.notice_text)}, index={self.index}, slot={self.slot})"